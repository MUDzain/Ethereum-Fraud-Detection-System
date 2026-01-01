from flask import Flask, render_template_string, request, jsonify
import requests
import os
import sys
from web3 import Web3

# Add project root to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import API_CONFIG, WEB_CONFIG, BLOCKCHAIN_CONFIG

app = Flask(__name__)

# Initialize blockchain connection
def get_blockchain_connection():
    """Get Web3 connection to blockchain"""
    try:
        rpc_url = BLOCKCHAIN_CONFIG.get("rpc_url", "https://eth-sepolia.g.alchemy.com/v2/CJlM2xLQd6oOKAI2LcXoz")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if w3.is_connected():
            return w3
        else:
            return None
    except Exception as e:
        print(f"Blockchain connection error: {e}")
        return None

def get_contract():
    """Get the smart contract instance"""
    w3 = get_blockchain_connection()
    if not w3:
        return None
    
    try:
        contract_address = BLOCKCHAIN_CONFIG.get("contract_address", "0x6ac1340cD2eA7F334D037466249196E16d1d0bda")
        contract_abi = BLOCKCHAIN_CONFIG.get("contract_abi", [])
        checksum_address = Web3.to_checksum_address(contract_address)
        contract = w3.eth.contract(address=checksum_address, abi=contract_abi)
        return contract
    except Exception as e:
        print(f"Contract initialization error: {e}")
        return None

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ethereum Fraud Detection System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            display: none;
        }
        .result.fraud {
            background-color: #ffebee;
            border: 1px solid #f44336;
            color: #c62828;
        }
        .result.legitimate {
            background-color: #e8f5e8;
            border: 1px solid #4caf50;
            color: #2e7d32;
        }
        .result.error {
            background-color: #fff3e0;
            border: 1px solid #ff9800;
            color: #e65100;
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        .stat-label {
            color: #7f8c8d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Ethereum Fraud Detection System</h1>
        <p style="text-align: center; color: #7f8c8d; margin-bottom: 30px;">
            Reading fraud assessments from Ethereum Sepolia Blockchain
        </p>
        
        <form id="fraudForm">
            <div class="form-group">
                <label for="address">Ethereum Wallet Address:</label>
                <input type="text" id="address" name="address"
                       placeholder="0x..." required
                       pattern="0x[a-fA-F0-9]{40}"
                       title="Please enter a valid Ethereum address">
            </div>
            <button type="submit">🔍 Check for Fraud</button>
        </form>
        
        <div id="result" class="result"></div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="totalAddresses">-</div>
                <div class="stat-label">Total Addresses</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="fraudRatio">-</div>
                <div class="stat-label">Fraud Ratio</div>
            </div>
        </div>
    </div>

    <script>
        // Load model statistics on page load
        window.onload = function() {
            loadModelStats();
        };

        function loadModelStats() {
            fetch('/model_info')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('totalAddresses').textContent = data.dataset_size.toLocaleString();
                    document.getElementById('fraudRatio').textContent = (data.fraud_ratio * 100).toFixed(1) + '%';
                })
                .catch(error => {
                    console.error('Error loading model stats:', error);
                });
        }

        document.getElementById('fraudForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const address = document.getElementById('address').value;
            const resultDiv = document.getElementById('result');
            
            // Show loading state
            resultDiv.style.display = 'block';
            resultDiv.className = 'result';
            resultDiv.innerHTML = '🔍 Analyzing address...';
            
            // Make API call
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({address: address})
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        // Return error data with status
                        return Promise.reject({...data, httpStatus: response.status});
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    const isFraud = data.prediction === 1;
                    
                    resultDiv.className = `result ${isFraud ? 'fraud' : 'legitimate'}`;
                    
                    // Format blockchain data
                    const hasMLPrediction = data.hasMLPrediction ? 'Yes' : 'No';
                    const mlConfidence = data.mlConfidence ? (data.mlConfidence / 100).toFixed(2) : 'N/A';
                    const reputationScore = data.reputationScore ? (data.reputationScore / 100).toFixed(1) : 'N/A';
                    const reportCount = data.reportCount || 0;
                    const overallRisk = data.overallRisk ? (data.overallRisk / 100).toFixed(2) : 'N/A';
                    const timestamp = data.mlTimestamp ? new Date(data.mlTimestamp * 1000).toLocaleString() : 'N/A';
                    
                    // Determine risk level
                    let riskLevel = 'N/A';
                    let riskColor = '#666';
                    if (data.overallRisk !== null && data.overallRisk !== undefined) {
                        if (data.overallRisk < 3000) {
                            riskLevel = 'LOW';
                            riskColor = '#4caf50';
                        } else if (data.overallRisk < 7000) {
                            riskLevel = 'MEDIUM';
                            riskColor = '#ff9800';
                        } else {
                            riskLevel = 'HIGH';
                            riskColor = '#f44336';
                        }
                    }
                    
                    let htmlContent = `
                        <h3>${isFraud ? '🚨 FRAUDULENT' : '✅ LEGITIMATE'}</h3>
                        <p><strong>Address:</strong> ${data.address}</p>
                        <hr style="margin: 15px 0; border: none; border-top: 1px solid #ddd;">
                        <h4>Blockchain Data:</h4>
                        <p><strong>Has ML Prediction:</strong> ${hasMLPrediction}</p>
                        <p><strong>ML Prediction:</strong> ${isFraud ? 'Fraudulent' : 'Legitimate'}</p>
                        <p><strong>ML Confidence:</strong> ${mlConfidence}%</p>
                        <p><strong>Reputation Score:</strong> ${reputationScore}%</p>
                        <p><strong>Report Count:</strong> ${reportCount}</p>
                        <p><strong>Overall Risk:</strong> ${overallRisk}% <span style="color: ${riskColor}; font-weight: bold;">(${riskLevel})</span></p>
                        <p><strong>Last Updated:</strong> ${timestamp}</p>
                        <hr style="margin: 15px 0; border: none; border-top: 1px solid #ddd;">
                        <p><strong>Source:</strong> Ethereum Sepolia Blockchain</p>
                    `;
                    
                    resultDiv.innerHTML = htmlContent;
                } else if (data.status === 'not_found') {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `
                        <h3>⚠️ Address Not Found on Blockchain</h3>
                        <p><strong>Address:</strong> ${data.address}</p>
                        <p>${data.error || 'This address has not been processed by the oracle service yet.'}</p>
                        <p style="margin-top: 15px; font-size: 14px; color: #666;">
                            The oracle service needs to process this address and write the ML prediction to the blockchain.
                            Please check back later or verify the address is being monitored by the oracle.
                        </p>
                    `;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `
                        <h3>❌ Error</h3>
                        <p>${data.error || 'Unknown error occurred'}</p>
                    `;
                }
            })
            .catch(error => {
                resultDiv.className = 'result error';
                
                // Handle structured error responses
                if (error.status === 'not_found') {
                    resultDiv.innerHTML = `
                        <h3>⚠️ Address Not Found on Blockchain</h3>
                        <p><strong>Address:</strong> ${error.address || 'Unknown'}</p>
                        <p>${error.error || 'This address has not been processed by the oracle service yet.'}</p>
                        <p style="margin-top: 15px; font-size: 14px; color: #666;">
                            The oracle service needs to process this address and write the ML prediction to the blockchain.
                            Please check back later or verify the address is being monitored by the oracle.
                        </p>
                    `;
                } else {
                    resultDiv.innerHTML = `
                        <h3>❌ Error</h3>
                        <p>${error.error || 'Failed to connect to the fraud detection service.'}</p>
                    `;
                }
                console.error('Error:', error);
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict_fraud():
    """Read fraud assessment from blockchain"""
    try:
        data = request.get_json()
        address = data.get('address')
        
        if not address:
            return jsonify({"error": "Address is required"}), 400
        
        # Get contract instance
        contract = get_contract()
        if not contract:
            return jsonify({
                "error": "Cannot connect to blockchain",
                "status": "error"
            }), 503
        
        # Convert address to checksum format
        try:
            checksum_address = Web3.to_checksum_address(address)
        except Exception as e:
            return jsonify({
                "error": f"Invalid Ethereum address: {str(e)}",
                "status": "error"
            }), 400
        
        # Read from blockchain
        try:
            assessment = contract.functions.getFraudAssessment(checksum_address).call()
            
            # Parse assessment data
            hasMLPrediction = assessment[0]
            mlIsFraudulent = assessment[1]
            mlConfidence = assessment[2]
            mlTimestamp = assessment[3]
            reputationScore = assessment[4]
            reportCount = assessment[5]
            overallRisk = assessment[6]
            
            # Check if address has been assessed
            if not hasMLPrediction:
                return jsonify({
                    "error": "Address not found on blockchain. The oracle service may not have processed this address yet.",
                    "address": address,
                    "status": "not_found"
                }), 404
            
            # Return blockchain data
            return jsonify({
                "address": address,
                "prediction": 1 if mlIsFraudulent else 0,
                "probability": mlConfidence / 10000.0,  # Convert from basis points (0-10000) to 0-1
                "hasMLPrediction": hasMLPrediction,
                "mlIsFraudulent": mlIsFraudulent,
                "mlConfidence": mlConfidence,
                "mlTimestamp": mlTimestamp,
                "reputationScore": reputationScore,
                "reportCount": reportCount,
                "overallRisk": overallRisk,
                "status": "success",
                "source": "blockchain"
            })
            
        except Exception as e:
            return jsonify({
                "error": f"Error reading from blockchain: {str(e)}",
                "status": "error"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "status": "error"
        }), 500

@app.route('/model_info')
def model_info():
    """Proxy to get model information"""
    try:
        ml_api_url = f"http://{API_CONFIG['host']}:{API_CONFIG['port']}/model_info"
        response = requests.get(ml_api_url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"error": "Failed to get model info"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Cannot connect to ML API"}), 503

if __name__ == '__main__':
    print("Starting Web Interface...")
    print(f"Web interface will be available at: http://{WEB_CONFIG['host']}:{WEB_CONFIG['port']}")

    # Test blockchain connection
    print("\nTesting blockchain connection...")
    w3 = get_blockchain_connection()
    if w3:
        print(f"Connected to blockchain (Block: {w3.eth.block_number})")
        contract = get_contract()
        if contract:
            contract_address = BLOCKCHAIN_CONFIG.get("contract_address", "0x6ac1340cD2eA7F334D037466249196E16d1d0bda")
            print(f"Contract loaded: {contract_address}")
        else:
            print("Warning: Could not load contract (check contract address)")
    else:
        print("Warning: Could not connect to blockchain (check RPC URL)")

    print("\nThe web interface now reads fraud assessments from the blockchain!")
    print("   Make sure your contract is deployed and the oracle service has updated addresses.\n")
    
    app.run(host=WEB_CONFIG['host'], port=WEB_CONFIG['port'], debug=WEB_CONFIG['debug'], threaded=WEB_CONFIG['threaded'])
