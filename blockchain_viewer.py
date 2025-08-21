#!/usr/bin/env python3
"""
Blockchain Viewer for Fraud Detection System
This script allows you to view fraud assessments stored on the blockchain
"""

import os
import sys
from pathlib import Path
from web3 import Web3

# Set environment variables
os.environ['CONTRACT_ADDRESS'] = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
os.environ['RPC_URL'] = "http://localhost:8545"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

def print_info(message):
    print(f"INFO: {message}")

def print_success(message):
    print(f"SUCCESS: {message}")

def print_error(message):
    print(f"ERROR: {message}")

def connect_to_blockchain():
    """Connect to the local blockchain"""
    try:
        w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
        if w3.is_connected():
            print_success("Connected to local blockchain")
            print_info(f"Current block: {w3.eth.block_number}")
            return w3
        else:
            print_error("Failed to connect to blockchain")
            return None
    except Exception as e:
        print_error(f"Connection error: {e}")
        return None

def get_contract():
    """Get the smart contract instance"""
    w3 = connect_to_blockchain()
    if not w3:
        return None
    
    contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
    checksum_address = Web3.to_checksum_address(contract_address)
    
    # Contract ABI for reading data
    contract_abi = [
        {
            "inputs": [{"name": "_wallet", "type": "address"}],
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
            "inputs": [{"name": "_wallet", "type": "address"}],
            "name": "getReputation",
            "outputs": [{"name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"name": "_wallet", "type": "address"}],
            "name": "getReportCount",
            "outputs": [{"name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    
    contract = w3.eth.contract(address=checksum_address, abi=contract_abi)
    return contract

def view_address_assessment(address):
    """View fraud assessment for a specific address"""
    contract = get_contract()
    if not contract:
        return
    
    try:
        checksum_address = Web3.to_checksum_address(address)
        assessment = contract.functions.getFraudAssessment(checksum_address).call()
        
        print_header(f"Fraud Assessment for {address}")
        
        # Display assessment data
        print(f"Has ML Prediction: {'Yes' if assessment[0] else 'No'}")
        print(f"ML Fraudulent: {'YES' if assessment[1] else 'NO'}")
        print(f"ML Confidence: {assessment[2]}%")
        print(f"Timestamp: {assessment[3]}")
        print(f"Reputation Score: {assessment[4]/100:.1f}%")
        print(f"Report Count: {assessment[5]}")
        print(f"Overall Risk: {assessment[6]}")
        
        # Risk level interpretation
        risk = assessment[6]
        if risk < 3000:
            risk_level = "LOW RISK"
        elif risk < 7000:
            risk_level = "MEDIUM RISK"
        else:
            risk_level = "HIGH RISK"
        
        print(f"Risk Level: {risk_level}")
        
    except Exception as e:
        print_error(f"Error reading assessment: {e}")

def view_multiple_addresses():
    """View assessments for multiple test addresses"""
    contract = get_contract()
    if not contract:
        return
    
    test_addresses = [
        "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8",
        "0x0002b44ddb1476db43c868bd494422ee4c136fed",
        "0x0002bda54cb772d040f779e88eb453cac0daa244"
    ]
    
    print_header("Multiple Address Assessments")
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\nAddress {i}: {address}")
        print("-" * 40)
        
        try:
            checksum_address = Web3.to_checksum_address(address)
            assessment = contract.functions.getFraudAssessment(checksum_address).call()
            
            if assessment[0]:  # Has ML prediction
                fraud_status = "FRAUDULENT" if assessment[1] else "LEGITIMATE"
                confidence = f"{assessment[2]}%"
                risk_level = "Low" if assessment[6] < 3000 else "Medium" if assessment[6] < 7000 else "High"
                
                print(f"   Status: {fraud_status}")
                print(f"   Confidence: {confidence}")
                print(f"   Risk Level: {risk_level}")
                print(f"   Reputation: {assessment[4]/100:.1f}%")
            else:
                print("   No assessment available")
                
        except Exception as e:
            print(f"   ERROR: {e}")

def interactive_mode():
    """Interactive mode to check any address"""
    contract = get_contract()
    if not contract:
        return
    
    print_header("Interactive Blockchain Viewer")
    print_info("Enter Ethereum addresses to check their fraud assessment")
    print_info("Type 'quit' to exit")
    print_info("Type 'list' to see test addresses")
    
    while True:
        try:
            user_input = input("\nEnter address (or command): ").strip()
            
            if user_input.lower() == 'quit':
                print_info("Goodbye!")
                break
            elif user_input.lower() == 'list':
                print_info("Test addresses:")
                print("  0x00009277775ac7d0d59eaad8fee3d10ac6c805e8")
                print("  0x0002b44ddb1476db43c868bd494422ee4c136fed")
                print("  0x0002bda54cb772d040f779e88eb453cac0daa244")
                continue
            elif not user_input:
                continue
            
            # Validate address format
            if not user_input.startswith('0x') or len(user_input) != 42:
                print_error("Invalid address format. Must be 0x followed by 40 hex characters.")
                continue
            
            view_address_assessment(user_input)
            
        except KeyboardInterrupt:
            print_info("\nGoodbye!")
            break
        except Exception as e:
            print_error(f"Error: {e}")

def main():
    """Main function"""
    print_header("Blockchain Viewer for Fraud Detection System")
    
    # Check if blockchain is running
    w3 = connect_to_blockchain()
    if not w3:
        print_error("Please make sure your local blockchain is running:")
        print_info("Run: npx hardhat node")
        return
    
    print_success("Blockchain connection successful!")
    print_info("Contract Address: 0x5FbDB2315678afecb367f032d93F642f64180aa3")
    
    # Show menu
    print("\nChoose an option:")
    print("1. View test addresses")
    print("2. Interactive mode (check any address)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                view_multiple_addresses()
            elif choice == '2':
                interactive_mode()
                break
            elif choice == '3':
                print_info("Goodbye!")
                break
            else:
                print_error("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print_info("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
