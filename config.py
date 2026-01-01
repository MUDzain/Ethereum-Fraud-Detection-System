"""
Configuration file for Ethereum Fraud Detection System
This file centralizes all configuration settings to avoid hardcoded paths
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
CONTRACTS_DIR = PROJECT_ROOT / "contracts"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# Model paths
MODEL_PATHS = [
    RESULTS_DIR / "tuned_fraud_detection_model.joblib",
    RESULTS_DIR / "fraud_detection_model.joblib"
]

# Data files
CLEANED_DATA_PATH = DATA_DIR / "cleaned_data.csv"
TRANSACTION_DATASET_PATH = DATA_DIR / "transaction_dataset.csv"

# API Configuration
API_CONFIG = {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": True,
    "threaded": True
}

# Web Interface Configuration
WEB_CONFIG = {
    "host": "127.0.0.1", 
    "port": 8081,
    "debug": True,
    "threaded": True
}

# Oracle Service Configuration
ORACLE_CONFIG = {
    "api_url": "http://localhost:5000",
    "rpc_url": "http://localhost:8545",
    "sleep_interval": 3600,  # 60 minutes in seconds
    "gas_limit": 200000,
    "default_reputation_score": 5000,
    "default_report_count": 0
}

# Blockchain Configuration
BLOCKCHAIN_CONFIG = {
    "rpc_url": os.getenv("RPC_URL", "https://eth-sepolia.g.alchemy.com/v2/CJlM2xLQd6oOKAI2LcXoz"),
    "contract_address": os.getenv("CONTRACT_ADDRESS", "0x6ac1340cD2eA7F334D037466249196E16d1d0bda"),
    "contract_abi": [
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
        }
    ]
}

# Test Configuration
TEST_CONFIG = {
    "temp_dir_prefix": "fraud_detection_test_",
    "test_data_samples": 100,
    "test_features": 5,
    "random_seed": 42
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

def get_first_existing_path(candidates):
    """Get the first existing path from a list of candidates"""
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None

def get_model_path():
    """Get the path to the model file"""
    return get_first_existing_path(MODEL_PATHS)

def get_data_path():
    """Get the path to the cleaned data file"""
    return CLEANED_DATA_PATH

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [DATA_DIR, RESULTS_DIR, CONTRACTS_DIR, SCRIPTS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
