#!/usr/bin/env python3
"""
Simple script to read wallet fraud scores from the blockchain
This demonstrates how to read data from your smart contract
"""

import os
from web3 import Web3

# Configuration
RPC_URL = os.getenv("RPC_URL", "http://localhost:8545")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0x5FbDB2315678afecb367f032d93F642f64180aa3")

# Contract ABI (minimal - only what we need to read)
CONTRACT_ABI = [
    {
        "inputs": [{"name": "walletAddress", "type": "address"}],
        "name": "getFraudAssessment",
        "outputs": [
            {"name": "hasMLPrediction", "type": "bool"},
            {"name": "mlIsFraudulent", "type": "bool"},
            {"name": "mlConfidence", "type": "uint256"},
            {"name": "mlTimestamp", "type": "uint256"},
            {"name": "reputationScore", "type": "uint256"},
            {"name": "reportCount", "type": "uint256"},
            {"name": "overallRisk", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "walletAddress", "type": "address"}],
        "name": "getReputation",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "walletAddress", "type": "address"}],
        "name": "getReportCount",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def read_wallet_score(wallet_address):
    """
    Read wallet fraud score from blockchain
    
    Args:
        wallet_address: Ethereum wallet address to check
        
    Returns:
        Dictionary with wallet assessment data
    """
    # Connect to blockchain
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if not w3.is_connected():
        print("ERROR: Cannot connect to blockchain")
        print(f"Please check your RPC URL: {RPC_URL}")
        return None
    
    print(f"SUCCESS: Connected to blockchain")
    print(f"Current block: {w3.eth.block_number}")
    
    # Get contract instance
    checksum_contract = Web3.to_checksum_address(CONTRACT_ADDRESS)
    checksum_wallet = Web3.to_checksum_address(wallet_address)
    
    contract = w3.eth.contract(address=checksum_contract, abi=CONTRACT_ABI)
    
    try:
        # READ OPERATION: Get full fraud assessment
        assessment = contract.functions.getFraudAssessment(checksum_wallet).call()
        
        # Parse the results
        has_ml_prediction = assessment[0]
        is_fraudulent = assessment[1]
        ml_confidence = assessment[2]  # 0-10000 (basis points)
        timestamp = assessment[3]
        reputation = assessment[4]  # 0-10000 (basis points)
        report_count = assessment[5]
        overall_risk = assessment[6]  # 0-10000 (basis points)
        
        # Calculate percentages
        confidence_pct = ml_confidence / 100
        reputation_pct = reputation / 100
        risk_pct = overall_risk / 100
        
        # Determine risk level
        if risk_pct < 30:
            risk_level = "LOW RISK"
        elif risk_pct < 70:
            risk_level = "MEDIUM RISK"
        else:
            risk_level = "HIGH RISK"
        
        # Display results
        print("\n" + "="*60)
        print(f"WALLET FRAUD ASSESSMENT")
        print("="*60)
        print(f"Wallet Address: {wallet_address}")
        print(f"\nML Prediction:")
        print(f"  Has Prediction: {'Yes' if has_ml_prediction else 'No'}")
        if has_ml_prediction:
            print(f"  Is Fraudulent: {'YES' if is_fraudulent else 'NO'}")
            print(f"  Confidence: {confidence_pct:.1f}%")
            print(f"  Timestamp: {timestamp}")
        
        print(f"\nReputation:")
        print(f"  Score: {reputation_pct:.1f}%")
        print(f"  Reports: {report_count}")
        
        print(f"\nOverall Risk:")
        print(f"  Risk Score: {risk_pct:.1f}%")
        print(f"  Risk Level: {risk_level}")
        print("="*60)
        
        # Return structured data
        return {
            "wallet_address": wallet_address,
            "has_ml_prediction": has_ml_prediction,
            "is_fraudulent": is_fraudulent,
            "ml_confidence": confidence_pct,
            "reputation": reputation_pct,
            "report_count": report_count,
            "overall_risk": risk_pct,
            "risk_level": risk_level
        }
        
    except Exception as e:
        print(f"ERROR: Failed to read assessment: {e}")
        return None

def read_reputation_only(wallet_address):
    """Read only reputation score (simpler example)"""
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        return None
    
    checksum_contract = Web3.to_checksum_address(CONTRACT_ADDRESS)
    checksum_wallet = Web3.to_checksum_address(wallet_address)
    contract = w3.eth.contract(address=checksum_contract, abi=CONTRACT_ABI)
    
    try:
        reputation = contract.functions.getReputation(checksum_wallet).call()
        return reputation / 100  # Convert to percentage
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    """Main function"""
    print("="*60)
    print("BLOCKCHAIN WALLET SCORE READER")
    print("="*60)
    print(f"Contract: {CONTRACT_ADDRESS}")
    print(f"RPC URL: {RPC_URL}")
    print()
    
    # Test addresses (from your dataset)
    test_addresses = [
        "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8",
        "0x0002b44ddb1476db43c868bd494422ee4c136fed",
        "0x0002bda54cb772d040f779e88eb453cac0daa244"
    ]
    
    # Read scores for test addresses
    print("Reading wallet scores from blockchain...\n")
    
    for address in test_addresses:
        result = read_wallet_score(address)
        if result:
            print(f"\nQuick Summary for {address[:10]}...")
            print(f"  Fraudulent: {result['is_fraudulent']}")
            print(f"  Risk: {result['risk_level']} ({result['overall_risk']:.1f}%)")
        print()
    
    # Interactive mode
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("Enter wallet addresses to check (or 'quit' to exit)")
    
    while True:
        try:
            user_input = input("\nEnter address: ").strip()
            
            if user_input.lower() == 'quit':
                break
            
            if not user_input.startswith('0x') or len(user_input) != 42:
                print("ERROR: Invalid address format")
                continue
            
            read_wallet_score(user_input)
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()

