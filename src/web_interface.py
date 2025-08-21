from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

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
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const isFraud = data.prediction === 1;
                    const confidence = data.probability ? (data.probability * 100).toFixed(1) : 'N/A';
                    
                    resultDiv.className = `result ${isFraud ? 'fraud' : 'legitimate'}`;
                    resultDiv.innerHTML = `
                        <h3>${isFraud ? '🚨 FRAUDULENT' : '✅ LEGITIMATE'}</h3>
                        <p><strong>Address:</strong> ${data.address}</p>
                        <p><strong>Confidence:</strong> ${confidence}%</p>
                        <p><strong>Analysis:</strong> ${isFraud ?
                            'This wallet shows patterns consistent with fraudulent activity.' :
                            'This wallet appears to be conducting legitimate transactions.'}</p>
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
                resultDiv.innerHTML = `
                    <h3>❌ Error</h3>
                    <p>Failed to connect to the fraud detection service.</p>
                `;
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
    """Proxy to the ML API"""
    try:
        data = request.get_json()
        address = data.get('address')
        
        if not address:
            return jsonify({"error": "Address is required"}), 400
        
        # Call the ML API
        ml_api_url = "http://localhost:5000/predict"
        response = requests.post(ml_api_url, json={"address": address}, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"error": "ML API error", "details": response.text}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Cannot connect to ML API", "details": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/model_info')
def model_info():
    """Proxy to get model information"""
    try:
        ml_api_url = "http://localhost:5000/model_info"
        response = requests.get(ml_api_url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({"error": "Failed to get model info"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Cannot connect to ML API"}), 503

if __name__ == '__main__':
    print("🌐 Starting Web Interface...")
    print("Web interface will be available at: http://localhost:8081")
    print("Make sure your ML API is running at: http://localhost:5000")
    app.run(host='0.0.0.0', port=8081, debug=True)
