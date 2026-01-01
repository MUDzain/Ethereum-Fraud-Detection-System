# How to Check Data from Blockchain

This guide shows you exactly how to read wallet fraud scores from the blockchain.

---

## 🎯 Quick Start

### **Option 1: Using `read_wallet_score.py` (Easiest)**

#### **For Local Blockchain (Hardhat)**

1. **Start your local blockchain** (if not running):
   ```bash
   npx hardhat node
   ```

2. **Run the script**:
   ```bash
   python read_wallet_score.py
   ```

3. **The script will**:
   - Connect to `http://localhost:8545`
   - Read wallet scores for test addresses
   - Show you interactive mode to check any address

#### **For Sepolia Testnet**

1. **Set environment variables**:
   ```powershell
   $env:RPC_URL="https://eth-sepolia.g.alchemy.com/v2/YourKey"
   $env:CONTRACT_ADDRESS="0xYourContractAddress"
   ```

2. **Run the script**:
   ```bash
   python read_wallet_score.py
   ```

---

### **Option 2: Using `blockchain_viewer.py` (Interactive)**

#### **For Local Blockchain**

1. **Start your local blockchain**:
   ```bash
   npx hardhat node
   ```

2. **Run the viewer**:
   ```bash
   python blockchain_viewer.py
   ```

3. **Choose from menu**:
   - Option 1: View test addresses
   - Option 2: Interactive mode (check any address)
   - Option 3: Exit

#### **For Sepolia Testnet**

1. **Set environment variables**:
   ```powershell
   $env:RPC_URL="https://eth-sepolia.g.alchemy.com/v2/YourKey"
   $env:CONTRACT_ADDRESS="0xYourContractAddress"
   ```

2. **Run the viewer**:
   ```bash
   python blockchain_viewer.py
   ```

---

### **Option 3: Using Python Code Directly**

Create a simple Python script:

```python
from web3 import Web3

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))  # Local
# OR
# w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/YourKey"))  # Sepolia

# Contract address
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Local
# OR your Sepolia contract address

# Wallet to check
wallet_address = "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8"

# Contract ABI (minimal)
contract_abi = [
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

# Get contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Read from blockchain
checksum_address = Web3.to_checksum_address(wallet_address)
assessment = contract.functions.getFraudAssessment(checksum_address).call()

# Display results
print(f"Has ML Prediction: {assessment[0]}")
print(f"Is Fraudulent: {assessment[1]}")
print(f"Confidence: {assessment[2]/100}%")
print(f"Reputation: {assessment[4]/100}%")
print(f"Reports: {assessment[5]}")
print(f"Risk Score: {assessment[6]/100}%")
```

---

## 📋 Step-by-Step Example

### **Example: Check a Wallet on Local Blockchain**

1. **Make sure Hardhat node is running**:
   ```bash
   npx hardhat node
   ```
   (Keep this terminal open)

2. **Open a new terminal** and run:
   ```bash
   python read_wallet_score.py
   ```

3. **You'll see**:
   ```
   ============================================================
   BLOCKCHAIN WALLET SCORE READER
   ============================================================
   Contract: 0x5FbDB2315678afecb367f032d93F642f64180aa3
   RPC URL: http://localhost:8545

   Reading wallet scores from blockchain...

   SUCCESS: Connected to blockchain
   Current block: 123

   ============================================================
   WALLET FRAUD ASSESSMENT
   ============================================================
   Wallet Address: 0x00009277775ac7d0d59eaad8fee3d10ac6c805e8

   ML Prediction:
     Has Prediction: Yes
     Is Fraudulent: YES
     Confidence: 85.0%
     Timestamp: 1234567890

   Reputation:
     Score: 50.0%
     Reports: 0

   Overall Risk:
     Risk Score: 34.0%
     Risk Level: MEDIUM RISK
   ============================================================
   ```

4. **In interactive mode**, enter any address to check:
   ```
   Enter address: 0x0002b44ddb1476db43c868bd494422ee4c136fed
   ```

---

## 🔍 For Sepolia Testnet

### **Step 1: Get Your Contract Address**
Your contract was deployed to Sepolia. Find the address from:
- Your deployment output
- Etherscan (if you verified it)
- Your deployment script output

### **Step 2: Set Environment Variables**
```powershell
# In PowerShell
$env:RPC_URL="https://eth-sepolia.g.alchemy.com/v2/CJlM2xLQd6oOKAI2LcXoz"
$env:CONTRACT_ADDRESS="0xYourDeployedContractAddress"
```

### **Step 3: Run the Script**
```bash
python read_wallet_score.py
```

---

## ✅ What You'll See

When you read from blockchain, you get:

1. **ML Prediction**:
   - Has prediction? (Yes/No)
   - Is fraudulent? (YES/NO)
   - Confidence level (0-100%)

2. **Reputation**:
   - Reputation score (0-100%)
   - Number of reports

3. **Risk Assessment**:
   - Overall risk score (0-100%)
   - Risk level (LOW/MEDIUM/HIGH)

---

## 🛠️ Troubleshooting

### **Error: Cannot connect to blockchain**

**Solution**: Make sure your blockchain is running:
- **Local**: Run `npx hardhat node`
- **Sepolia**: Check your RPC URL is correct

### **Error: Invalid contract address**

**Solution**: 
- For local: Use `0x5FbDB2315678afecb367f032d93F642f64180aa3`
- For Sepolia: Use your deployed contract address

### **Error: No assessment available**

**Solution**: The wallet hasn't been processed yet. Run the Oracle Service first:
```bash
python src/oracle_service.py
```

---

## 📝 Quick Reference

| Tool | Use Case | Command |
|------|----------|---------|
| `read_wallet_score.py` | Simple reading, batch checking | `python read_wallet_score.py` |
| `blockchain_viewer.py` | Interactive menu, multiple addresses | `python blockchain_viewer.py` |
| Direct Web3 code | Custom scripts, integration | See Option 3 above |

---

## 🎯 Summary

**To check from blockchain:**

1. **Make sure blockchain is running** (local or connected to Sepolia)
2. **Set contract address** (if using Sepolia)
3. **Run one of the tools**:
   - `python read_wallet_score.py` (easiest)
   - `python blockchain_viewer.py` (interactive)
4. **Enter wallet address** to check
5. **See the results** - fraud status, confidence, risk score

**That's it!** The blockchain will tell you the wallet score instantly (no gas cost for reading).

