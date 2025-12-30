# Blockchain Read & Write Operations Guide

## Overview
The smart contract supports both **READ** (view) and **WRITE** (transaction) operations. This guide explains what you can do and how to do it.

---

## 📖 READ Operations (No Gas Cost)

These operations **read data** from the blockchain. They don't modify anything and are **FREE** (no gas cost).

### 1. **getFraudAssessment(address)** - Get Complete Wallet Score
**Purpose**: Get the full fraud assessment for any wallet address.

**Returns**:
- `hasMLPrediction` - Whether ML prediction exists (bool)
- `mlIsFraudulent` - Is wallet fraudulent? (bool)
- `mlConfidence` - ML confidence score 0-10000 (0-100%)
- `mlTimestamp` - When prediction was made
- `reputationScore` - Reputation score 0-10000 (0-100%)
- `reportCount` - Number of reports
- `overallRisk` - Overall risk score 0-10000 (0-100%)

**Example Usage**:
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
wallet_address = "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8"

# Get contract instance (you need the ABI)
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Read the assessment
assessment = contract.functions.getFraudAssessment(wallet_address).call()

print(f"Fraudulent: {assessment[1]}")
print(f"Confidence: {assessment[2]}%")
print(f"Risk Score: {assessment[6]}")
```

### 2. **getReputation(address)** - Get Reputation Score Only
**Purpose**: Get just the reputation score for a wallet.

**Returns**: Reputation score (0-10000, where 10000 = 100%)

**Example**:
```python
reputation = contract.functions.getReputation(wallet_address).call()
print(f"Reputation: {reputation/100}%")
```

### 3. **getReportCount(address)** - Get Report Count
**Purpose**: Get how many times a wallet has been reported.

**Returns**: Number of reports (uint256)

**Example**:
```python
reports = contract.functions.getReportCount(wallet_address).call()
print(f"Reports: {reports}")
```

### 4. **isAddressReported(address)** - Check if Reported
**Purpose**: Check if an address has ever been reported.

**Returns**: True/False (bool)

**Example**:
```python
is_reported = contract.functions.isAddressReported(wallet_address).call()
print(f"Is Reported: {is_reported}")
```

### 5. **getContractInfo()** - Get Contract Information
**Purpose**: Get contract owner, oracle address, and balance.

**Returns**: (owner address, oracle address, contract balance)

**Example**:
```python
info = contract.functions.getContractInfo().call()
owner, oracle, balance = info
print(f"Owner: {owner}")
print(f"Oracle: {oracle}")
```

---

## ✍️ WRITE Operations (Costs Gas)

These operations **modify data** on the blockchain. They require **gas fees** and must be signed with a private key.

### 1. **updateFraudAssessment(...)** - Write ML Predictions
**Purpose**: Oracle service writes ML predictions to blockchain.

**Who Can Call**: Only the Oracle address (set in constructor)

**Parameters**:
- `walletAddress` - Address to assess
- `hasMLPrediction` - Does ML prediction exist?
- `mlIsFraudulent` - Is it fraudulent?
- `mlConfidence` - Confidence 0-10000
- `reputationScore` - Reputation 0-10000
- `reportCount` - Number of reports
- `overallRisk` - Overall risk 0-10000

**Example** (from oracle_service.py):
```python
transaction = contract.functions.updateFraudAssessment(
    wallet_address,
    True,  # hasMLPrediction
    True,  # mlIsFraudulent
    8500,  # mlConfidence (85%)
    5000,  # reputationScore (50%)
    0,     # reportCount
    3400   # overallRisk (34%)
).build_transaction({
    'from': account.address,
    'gas': 200000,
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(account.address),
})
```

### 2. **reportAddress(address, reason)** - Report a Wallet
**Purpose**: Anyone can report a wallet as potentially fraudulent.

**Who Can Call**: Anyone (public function)

**Parameters**:
- `walletAddress` - Address to report
- `reason` - Reason for report (string)

**What It Does**:
- Increments report count
- Decreases reputation by 10%
- Updates overall risk score

**Example**:
```python
transaction = contract.functions.reportAddress(
    "0x00009277775ac7d0d59eaad8fee3d10ac6c805e8",
    "Suspicious transaction pattern"
).build_transaction({...})
```

### 3. **updateOracle(newOracle)** - Change Oracle Address
**Purpose**: Owner can change the oracle address.

**Who Can Call**: Only contract owner

**Example**:
```python
transaction = contract.functions.updateOracle(
    new_oracle_address
).build_transaction({...})
```

### 4. **transferOwnership(newOwner)** - Transfer Ownership
**Purpose**: Owner can transfer contract ownership.

**Who Can Call**: Only contract owner

### 5. **clearAssessment(address)** - Clear Assessment
**Purpose**: Owner can delete an assessment (emergency function).

**Who Can Call**: Only contract owner

---

## 🛠️ How to Use Existing Tools

### Option 1: Use `blockchain_viewer.py` (Easiest)
This script already reads from the blockchain:

```bash
# Set your contract address (if using Sepolia)
$env:CONTRACT_ADDRESS="0xYourContractAddress"
$env:RPC_URL="https://eth-sepolia.g.alchemy.com/v2/YourKey"

# Run the viewer
python blockchain_viewer.py
```

**Features**:
- View single address assessment
- View multiple addresses
- Interactive mode to check any address

### Option 2: Use Oracle Service's `get_blockchain_assessment()`
The oracle service has a built-in read function:

```python
from src.oracle_service import FraudDetectionOracle

oracle = FraudDetectionOracle(
    rpc_url="http://localhost:8545",
    contract_address="0xYourContractAddress"
)

assessment = oracle.get_blockchain_assessment("0x00009277775ac7d0d59eaad8fee3d10ac6c805e8")
print(assessment)
```

### Option 3: Direct Web3 Call (Advanced)
For custom scripts, use Web3 directly:

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
assessment = contract.functions.getFraudAssessment(wallet_address).call()
```

---

## 📊 Understanding the Wallet Score

When you read from the blockchain, you get:

1. **ML Prediction** (from your ML model)
   - Is it fraudulent? (True/False)
   - Confidence level (0-100%)

2. **Reputation Score** (0-100%)
   - Starts at 50% (5000/10000)
   - Decreases when reported
   - Increases over time (if implemented)

3. **Report Count**
   - How many times users reported this wallet

4. **Overall Risk Score** (0-100%)
   - Calculated from: ML (40%) + Reputation (30%) + Reports (30%)
   - **0-30%** = LOW RISK
   - **30-70%** = MEDIUM RISK
   - **70-100%** = HIGH RISK

---

## 🔄 Complete Flow

1. **Oracle Service** (WRITE):
   - Gets ML prediction from API
   - Writes to blockchain using `updateFraudAssessment()`

2. **Blockchain Viewer** (READ):
   - Reads from blockchain using `getFraudAssessment()`
   - Shows wallet score, risk level, reputation

3. **Users** (READ):
   - Can check any wallet address
   - Can report wallets (WRITE)

---

## ✅ Summary

**READ Operations** (Free, No Gas):
- ✅ `getFraudAssessment()` - Get full wallet score
- ✅ `getReputation()` - Get reputation only
- ✅ `getReportCount()` - Get report count
- ✅ `isAddressReported()` - Check if reported
- ✅ `getContractInfo()` - Get contract info

**WRITE Operations** (Costs Gas):
- ✅ `updateFraudAssessment()` - Oracle writes ML predictions
- ✅ `reportAddress()` - Users report wallets
- ✅ `updateOracle()` - Owner updates oracle
- ✅ `transferOwnership()` - Owner transfers ownership
- ✅ `clearAssessment()` - Owner clears assessment

**Yes, the blockchain can tell you the wallet score!** Just use `getFraudAssessment(address)` to read it.

