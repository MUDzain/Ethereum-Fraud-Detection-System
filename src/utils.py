"""
Utility functions for Ethereum Fraud Detection System
This module contains common utility functions used across the system
"""

import re
import json
import logging
from typing import Union, Any, Dict, List
from web3 import Web3

logger = logging.getLogger(__name__)

def is_valid_ethereum_address(address: str) -> bool:
    """
    Validate if a string is a valid Ethereum address format.
    
    Args:
        address: String to validate as Ethereum address
        
    Returns:
        bool: True if valid Ethereum address format, False otherwise
    """
    if not isinstance(address, str):
        return False
    
    # Basic check - starts with 0x and has right length (40 hex chars)
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False
    
    return True

def is_valid_json(json_str: str) -> bool:
    """
    Check if a string is valid JSON format.
    
    Args:
        json_str: String to validate as JSON
        
    Returns:
        bool: True if valid JSON, False otherwise
    """
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

def is_number(value: Any) -> bool:
    """
    Check if a value can be converted to a number.
    
    Args:
        value: Value to check
        
    Returns:
        bool: True if value is a number or can be converted to one, False otherwise
    """
    if isinstance(value, (int, float)):
        return True
    
    if isinstance(value, str):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    return False

def normalize_address(address: str) -> str:
    """
    Normalize an Ethereum address to lowercase for consistent storage/lookup.
    
    Args:
        address: Ethereum address to normalize
        
    Returns:
        str: Lowercase version of the address
        
    Raises:
        ValueError: If address is not a valid Ethereum address format
    """
    if not is_valid_ethereum_address(address):
        raise ValueError(f"Invalid Ethereum address format: {address}")
    
    return address.lower()

def checksum_address(address: str) -> str:
    """
    Convert an Ethereum address to checksum format.
    
    Args:
        address: Ethereum address to convert
        
    Returns:
        str: Checksummed version of the address
        
    Raises:
        ValueError: If address is not a valid Ethereum address format
    """
    if not is_valid_ethereum_address(address):
        raise ValueError(f"Invalid Ethereum address format: {address}")
    
    return Web3.to_checksum_address(address)

def calculate_risk_score(confidence: float, reputation_score: int = 5000, report_count: int = 0) -> int:
    """
    Calculate overall risk score based on ML confidence and other factors.
    
    Args:
        confidence: ML model confidence (0.0 to 1.0)
        reputation_score: Reputation score (0 to 10000)
        report_count: Number of reports against the address
        
    Returns:
        int: Calculated risk score (0 to 100)
    """
    # Base risk from ML confidence
    base_risk = int(confidence * 100) if confidence else 50
    
    # Adjust based on reputation (lower reputation = higher risk)
    reputation_factor = (10000 - reputation_score) / 10000
    
    # Adjust based on report count
    report_factor = min(report_count * 5, 50)  # Cap at 50 points
    
    # Combine factors
    risk_score = int(base_risk * 0.6 + reputation_factor * 30 + report_factor * 0.1)
    
    # Ensure score is within bounds
    return max(0, min(100, risk_score))

def format_prediction_result(address: str, prediction: int, probability: float = None) -> Dict[str, Any]:
    """
    Format prediction result into a standardized dictionary.
    
    Args:
        address: Ethereum address
        prediction: ML prediction (0 or 1)
        probability: ML probability (optional)
        
    Returns:
        dict: Formatted prediction result
    """
    return {
        "address": address,
        "prediction": int(prediction),
        "probability": float(probability) if probability is not None else None,
        "is_fraud": bool(prediction),
        "confidence_level": "high" if probability and probability > 0.8 else "medium" if probability and probability > 0.6 else "low"
    }

def validate_prediction_input(data: Dict[str, Any]) -> tuple[str, List[str]]:
    """
    Validate input data for prediction requests.
    
    Args:
        data: Input data dictionary
        
    Returns:
        tuple: (address, list_of_errors)
    """
    errors = []
    address = None
    
    if not isinstance(data, dict):
        errors.append("Input must be a JSON object")
        return address, errors
    
    if 'address' not in data:
        errors.append("Address is required")
    else:
        address = data['address']
        if not isinstance(address, str):
            errors.append("Address must be a string")
        elif not is_valid_ethereum_address(address):
            errors.append("Invalid Ethereum address format")
    
    return address, errors

def log_prediction_result(address: str, prediction: int, probability: float = None, source: str = "ML"):
    """
    Log prediction result with consistent format.
    
    Args:
        address: Ethereum address
        prediction: ML prediction (0 or 1)
        probability: ML probability (optional)
        source: Source of prediction (e.g., "ML", "Oracle")
    """
    fraud_status = "FRAUD" if prediction else "LEGITIMATE"
    prob_str = f" (confidence: {probability:.2f})" if probability else ""
    
    logger.info(f"{source} prediction for {address}: {fraud_status}{prob_str}")
