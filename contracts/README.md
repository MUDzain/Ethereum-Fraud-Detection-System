# Smart Contract and Blockchain Integration

This directory contains the smart contract I wrote for the Ethereum Fraud Detection System, along with deployment scripts.

## Files in This Directory

- **FraudDetectionContractV2.sol** - The main smart contract for fraud detection
- **../scripts/deploy_v2.js** - Script to deploy the contract
- **../hardhat.config.js** - Hardhat configuration file
- **../package.json** - Node.js dependencies

## What the Smart Contract Does

### Main Features
- Stores ML predictions and reputation scores on the blockchain
- Tracks wallet reputation scores (0-10000 scale)
- Lets users report suspicious addresses
- Calculates overall risk by combining ML predictions, reputation, and reports

### Key Functions
- `updateFraudAssessment()` - Oracle service calls this to update fraud data
- `getFraudAssessment()` - Get the complete fraud assessment for an address
- `getReputation()` - Get the reputation score for an address
- `reportAddress()` - Users can report suspicious addresses
- `calculateOverallRisk()` - Calculate the overall risk score

### Access Control
- **Owner**: Can update oracle address, transfer ownership, clear assessments
- **Oracle**: Can update fraud assessments (connects to my ML API)
- **Public**: Can view assessments and report addresses

## How to Deploy

### First, Install Dependencies
```bash
npm install
```

### Local Development
```bash
# Start a local blockchain
npx hardhat node

# Deploy to local network
npm run deploy:local
```

### Deploy to Sepolia Testnet
```bash
# Set up environment variables
export PRIVATE_KEY="your_private_key"
export SEPOLIA_URL="your_sepolia_rpc_url"

# Deploy to Sepolia
npm run deploy:sepolia
```

### Deploy to Mainnet (if needed)
```bash
# Set up environment variables
export PRIVATE_KEY="your_private_key"
export MAINNET_URL="your_mainnet_rpc_url"

# Deploy to mainnet
npm run deploy:mainnet
```

## How It Works with the ML System

The smart contract connects to my ML API through an oracle service:

1. **ML API** makes fraud predictions via REST endpoints
2. **Oracle Service** (in src/oracle_service.py) calls `updateFraudAssessment()` on the contract
3. **Web Interface** can read contract data to show real-time fraud status
4. **Blockchain Viewer** (blockchain_viewer.py) lets you inspect on-chain data

### Setting Up the Oracle Service
```bash
# Environment variables for oracle service
CONTRACT_ADDRESS=0x6ac1340cD2eA7F334D037466249196E16d1d0bda
RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
PRIVATE_KEY=your_private_key_here
ML_API_URL=http://localhost:5000
```

## Contract Addresses

### Sepolia Testnet (Where I Deployed)
- **Contract Address**: 0x6ac1340cD2eA7F334D037466249196E16d1d0bda
- **Etherscan**: https://sepolia.etherscan.io/address/0x6ac1340cD2eA7F334D037466249196E16d1d0bda
- **Oracle Address**: The address that can update fraud assessments
- **Owner Address**: My address with admin privileges

### Local Development
When you deploy locally, you'll get:
- **Contract Address**: The address where your contract is deployed
- **Oracle Address**: Address that can update fraud assessments
- **Owner Address**: Your address with admin privileges

## Security Features I Implemented

- **Access Control**: Only the oracle can update fraud assessments
- **Input Validation**: All inputs are checked for validity
- **Event Logging**: Important actions are logged as events
- **Emergency Functions**: Owner can clear assessments if needed

## Gas Optimization

- **Optimizer Enabled**: Reduces gas costs during deployment
- **Efficient Storage**: Uses packed structs to save gas
- **Batch Operations**: Supports batch updates for efficiency

## Why I Chose This Design

I wanted to create a system where:
- ML predictions are stored permanently on the blockchain
- Users can contribute by reporting suspicious addresses
- Reputation builds up over time
- Everything is transparent and verifiable

This combines the power of machine learning with the trust and transparency of blockchain technology.
