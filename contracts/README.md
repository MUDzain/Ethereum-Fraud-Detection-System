# Smart Contract and Blockchain Integration

This directory contains the smart contract and deployment scripts for the Ethereum Fraud Detection System.

## Files

- **`FraudDetectionContractV2.sol`** - Main smart contract for fraud detection
- **`../scripts/deploy_v2.js`** - Deployment script
- **`../hardhat.config.js`** - Hardhat configuration
- **`../package.json`** - Node.js dependencies

## Smart Contract Features

### Core Functionality
- **Fraud Assessment Storage**: Stores ML predictions and reputation scores
- **Reputation System**: Tracks wallet reputation scores (0-10000)
- **Report System**: Allows users to report suspicious addresses
- **Risk Calculation**: Combines ML predictions, reputation, and reports

### Key Functions
- `updateFraudAssessment()` - Oracle updates fraud data
- `getFraudAssessment()` - Get complete fraud assessment
- `getReputation()` - Get reputation score
- `reportAddress()` - Report suspicious address
- `calculateOverallRisk()` - Calculate risk score

### Access Control
- **Owner**: Can update oracle, transfer ownership, clear assessments
- **Oracle**: Can update fraud assessments (ML API integration)
- **Public**: Can view assessments and report addresses

## Deployment

### Prerequisites
```bash
npm install
```

### Local Development
```bash
# Start local blockchain
npx hardhat node

# Deploy to local network
npm run deploy:local
```

### Testnet Deployment (Sepolia)
```bash
# Set environment variables
export PRIVATE_KEY="your_private_key"
export SEPOLIA_URL="your_sepolia_rpc_url"

# Deploy to Sepolia
npm run deploy:sepolia
```

### Mainnet Deployment
```bash
# Set environment variables
export PRIVATE_KEY="your_private_key"
export MAINNET_URL="your_mainnet_rpc_url"

# Deploy to mainnet
npm run deploy:mainnet
```

## Integration with ML System

The smart contract integrates with your ML API through an oracle service:

1. **ML API** provides fraud predictions
2. **Oracle Service** calls `updateFraudAssessment()` on the contract
3. **Web Interface** can read contract data for real-time fraud status

## Contract Addresses

After deployment, you'll get:
- **Contract Address**: The deployed contract address
- **Oracle Address**: Address authorized to update fraud assessments
- **Owner Address**: Contract owner with administrative privileges

## Security Features

- **Access Control**: Only oracle can update fraud assessments
- **Input Validation**: All inputs are validated
- **Event Logging**: All important actions are logged
- **Emergency Functions**: Owner can clear assessments if needed

## Gas Optimization

- **Optimizer Enabled**: Reduces gas costs
- **Efficient Storage**: Uses packed structs where possible
- **Batch Operations**: Supports batch updates for efficiency
