import requests
import time
import json
import os
from web3 import Web3
from eth_account import Account
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudDetectionOracle:
    def __init__(self, api_url="http://localhost:5000", rpc_url=None, contract_address=None, private_key=None):
        self.api_url = api_url
        self.rpc_url = rpc_url or "http://localhost:8545"
        self.contract_address = contract_address
        self.private_key = private_key
        
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Load contract ABI (simplified for this example)
        self.contract_abi = [
            {
                "inputs": [
                    {"name": "walletAddress", "type": "address"},
                    {"name": "hasMLPrediction", "type": "bool"},
                    {"name": "mlIsFraudulent", "type": "bool"},
                    {"name": "mlConfidence", "type": "uint256"},
                    {"name": "reputationScore", "type": "uint256"},
                    {"name": "reportCount", "type": "uint256"},
                    {"name": "overallRisk", "type": "uint256"}
                ],
                "name": "updateFraudAssessment",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "_wallet", "type": "address"}],
                "name": "getFraudAssessment",
                "outputs": [
                    {"name": "hasMLPrediction", "type": "bool"},
                    {"name": "mlIsFraudulent", "type": "bool"},
                    {"name": "mlConfidence", "type": "uint256"},
                    {"name": "mlTimestamp", "type": "uint256"},
                    {"name": "reputationScore", "type": "int256"},
                    {"name": "reportCount", "type": "uint256"},
                    {"name": "overallRisk", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        if self.contract_address:
            # Ensure the contract address is checksummed
            self.contract_address = Web3.to_checksum_address(self.contract_address)
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=self.contract_abi
            )
        
        self._test_api_connection()
   
    def _test_api_connection(self):
        """Test connection to the ML API"""
        try:
            response = requests.get(f"{self.api_url}/health")
            if response.status_code == 200:
                logger.info("✅ ML API connection successful")
            else:
                logger.error("❌ ML API health check failed")
        except Exception as e:
            logger.error(f"❌ Cannot connect to ML API: {e}")
   
    def get_ml_prediction(self, address):
        """Get fraud prediction from ML API"""
        try:
            # The API expects a lowercase address
            response = requests.post(
                f"{self.api_url}/predict",
                json={"address": address},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "prediction": data["prediction"],
                    "probability": data["probability"],
                    "status": "success"
                }
            else:
                logger.error(f"API error for {address}: {response.text}")
                return {"status": "error", "message": response.text}
               
        except Exception as e:
            logger.error(f"Error getting prediction for {address}: {e}")
            return {"status": "error", "message": str(e)}
   
    def update_blockchain_prediction(self, address, prediction, confidence):
        """Update prediction on the blockchain"""
        if not self.contract_address or not self.private_key:
            logger.warning("Blockchain update skipped - no contract address or private key")
            return False
        
        try:
            account = Account.from_key(self.private_key)
            confidence_percentage = int(confidence * 100) if confidence else 50
            
            # Ensure the address is checksummed before the contract call
            checksum_address = Web3.to_checksum_address(address)
            
            # Calculate reputation score and report count (default values for now)
            reputation_score = 5000  # Default 50% reputation
            report_count = 0  # No reports yet
            overall_risk = int(confidence_percentage * 0.4)  # Simple risk calculation
            
            transaction = self.contract.functions.updateFraudAssessment(
                checksum_address,
                True,  # hasMLPrediction
                bool(prediction),  # mlIsFraudulent
                confidence_percentage,  # mlConfidence
                reputation_score,  # reputationScore
                report_count,  # reportCount
                overall_risk  # overallRisk
            ).build_transaction({
                'from': account.address,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(account.address),
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            # CORRECTED: The attribute is now 'raw_transaction'
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                logger.info(f"✅ Blockchain updated for {address}: Fraud={prediction}, Confidence={confidence_percentage}%")
                return True
            else:
                logger.error(f"❌ Transaction failed for {address}")
                return False
               
        except Exception as e:
            logger.error(f"Error updating blockchain for {address}: {e}")
            return False
   
    def process_address(self, address):
        """Process a single address through the oracle"""
        logger.info(f"Processing address: {address}")
        
        # The ML API expects a lowercase address, while the blockchain needs a checksum address.
        # We handle this distinction here.
        ml_result = self.get_ml_prediction(address.lower())
        
        if ml_result["status"] == "success":
            prediction = ml_result["prediction"]
            confidence = ml_result["probability"]
            
            blockchain_success = self.update_blockchain_prediction(address, prediction, confidence)
            
            return {
                "address": address,
                "ml_prediction": prediction,
                "ml_confidence": confidence,
                "blockchain_updated": blockchain_success
            }
        else:
            logger.error(f"Failed to get ML prediction for {address}: {ml_result.get('message', 'Unknown error')}")
            return {
                "address": address,
                "error": ml_result.get("message", "Unknown error")
            }
   
    def get_blockchain_assessment(self, address):
        """Get fraud assessment from blockchain"""
        if not self.contract_address:
            logger.warning("Cannot get blockchain assessment - no contract address")
            return None
        
        try:
            # Ensure the address is checksummed before the contract call
            checksum_address = Web3.to_checksum_address(address)
            assessment = self.contract.functions.getFraudAssessment(checksum_address).call()
            return {
                "hasMLPrediction": assessment[0],
                "mlIsFraudulent": assessment[1],
                "mlConfidence": assessment[2],
                "mlTimestamp": assessment[3],
                "reputationScore": assessment[4],
                "reportCount": assessment[5],
                "overallRisk": assessment[6]
            }
        except Exception as e:
            logger.error(f"Error getting blockchain assessment for {address}: {e}")
            return None

def main():
    """Main function to run the oracle service in a continuous loop."""
    print("🚀 Starting Fraud Detection Oracle Service...")
    
    # Configuration (can be set via environment variables)
    api_url = os.getenv("ML_API_URL", "http://localhost:5000")
    rpc_url = os.getenv("RPC_URL", "http://localhost:8545")
    contract_address = os.getenv("CONTRACT_ADDRESS")
    private_key = os.getenv("PRIVATE_KEY")
    
    oracle = FraudDetectionOracle(
        api_url=api_url,
        rpc_url=rpc_url,
        contract_address=contract_address,
        private_key=private_key
    )
    
    # These addresses are from your cleaned_data.csv file.
    test_addresses = [
        "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8",
        "0x0002b44ddb1476db43c868bd494422ee4c136fed",
        "0x0002bda54cb772d040f779e88eb453cac0daa244"
    ]
    
    # Run the oracle in a loop
    while True:
        print(f"Processing {len(test_addresses)} addresses...")
        for address in test_addresses:
            result = oracle.process_address(address)
            print(f"Result for {address}: {result}")
            
            assessment = oracle.get_blockchain_assessment(address)
            if assessment:
                print(f"Blockchain assessment: {assessment}")
            
            print("-" * 50)
        
        # Wait for 60 minutes before the next run
        print("😴 Processing complete. Sleeping for 60 minutes...")
        time.sleep(3600)  # 3600 seconds = 60 minutes

if __name__ == "__main__":
    main()
