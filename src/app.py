"""
Flask application for Ethereum Fraud Detection API
Created on: August 19, 2025
@author: MUDzain
@description: Web API for machine learning model that detects fraudulent blockchain transactions
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
import numpy as np
from flask_cors import CORS
import sys

# Add project root to path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import get_model_path, get_data_path, API_CONFIG, ensure_directories

app = Flask(__name__)
CORS(app)  # Enable CORS for blockchain integration

# Ensure directories exist
ensure_directories()

# Get paths from configuration
model_path = get_model_path()
data_path = get_data_path()

if not model_path:
    raise FileNotFoundError(
        "Model artifact not found. Please ensure a trained model exists in the results directory."
    )

# Load model (no scaler needed for Random Forest)
model = joblib.load(model_path)
scaler = None  # Random Forest doesn't require scaling

def transform_features(array_2d):
    # Apply scaler if available; otherwise pass-through
    if scaler is not None:
        return scaler.transform(array_2d)
    return array_2d

# Load the dataset for feature extraction
df = pd.read_csv(data_path)
feature_columns = df.drop(columns=['full_address', 'is_fraud']).select_dtypes(include='number').columns

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the API"""
    return jsonify({"status": "healthy", "message": "Fraud Detection API is running"})

@app.route('/predict', methods=['POST'])
def predict_fraud():
    """Predict fraud for a given wallet address"""
    try:
        data = request.get_json()
        address = data.get('address')
        
        if not address:
            return jsonify({"error": "Address is required"}), 400
        
        # FIX: Convert the incoming address to lowercase for the lookup
        address_data = df[df['full_address'] == address.lower()]
        
        if address_data.empty:
            return jsonify({
                "error": "Address not found in dataset",
                "address": address
            }), 404
        
        # Extract features
        features = address_data[feature_columns].values[0]
        features_scaled = transform_features(features.reshape(1, -1))
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1] if hasattr(model, 'predict_proba') else None
        
        return jsonify({
            "address": address,
            "prediction": int(prediction),
            "probability": float(probability) if probability is not None else None,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Predict fraud for multiple addresses"""
    try:
        data = request.get_json()
        addresses = data.get('addresses', [])
        
        if not addresses:
            return jsonify({"error": "Addresses list is required"}), 400
        
        results = []
        for address in addresses:
            # FIX: Convert the incoming address to lowercase for the lookup
            address_data = df[df['full_address'] == address.lower()]
            
            if address_data.empty:
                results.append({
                    "address": address,
                    "prediction": None,
                    "probability": None,
                    "error": "Address not found"
                })
                continue
            
            # Extract features
            features = address_data[feature_columns].values[0]
            features_scaled = transform_features(features.reshape(1, -1))
            
            # Make prediction
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0][1] if hasattr(model, 'predict_proba') else None
            
            results.append({
                "address": address,
                "prediction": int(prediction),
                "probability": float(probability) if probability is not None else None
            })
        
        return jsonify({
            "results": results,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get information about the model"""
    return jsonify({
        "model_type": "RandomForest",
        "feature_count": len(feature_columns),
        "feature_names": feature_columns.tolist(),
        "dataset_size": len(df),
        "fraud_ratio": float(df['is_fraud'].mean())
    })

if __name__ == '__main__':
    print("Starting Fraud Detection API...")
    print(f"Model loaded from: {model_path}")
    print(f"Dataset loaded with {len(df)} addresses")
    print(f"API will be available at: http://{API_CONFIG['host']}:{API_CONFIG['port']}")
    
    try:
        app.run(
            host=API_CONFIG['host'], 
            port=API_CONFIG['port'], 
            debug=API_CONFIG['debug'], 
            threaded=API_CONFIG['threaded']
        )
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        app.run(host='localhost', port=5000, debug=True, threaded=True)
