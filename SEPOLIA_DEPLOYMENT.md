# 🚀 Deploying to Ethereum Sepolia Testnet

This guide will help you deploy your Fraud Detection Smart Contract to the Ethereum Sepolia testnet.

## 📋 Prerequisites

### 1. Get Sepolia RPC URL
- **Infura** (Recommended): https://infura.io/
  1. Create free account
  2. Create new project
  3. Copy Sepolia endpoint URL
  4. Format: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`

- **Alchemy**: https://alchemy.com/
- **QuickNode**: https://quicknode.com/

### 2. Get Sepolia ETH
- **Sepolia Faucet**: https://sepoliafaucet.com/
- **Alchemy Faucet**: https://sepoliafaucet.com/
- You need ~0.1 Sepolia ETH for deployment

### 3. Get Etherscan API Key
- Go to: https://etherscan.io/
- Create account
- Get API key from your profile

## 🔧 Setup Environment Variables

Create a `.env` file in your project root:

```bash
# Sepolia Network Configuration
SEPOLIA_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
PRIVATE_KEY=your_private_key_here

# Etherscan API Key (for contract verification)
ETHERSCAN_API_KEY=your_etherscan_api_key_here
```

## 🚀 Deployment Steps

### Step 1: Compile Contracts
```bash
npx hardhat compile
```

### Step 2: Deploy to Sepolia
```bash
npx hardhat run scripts/deploy_sepolia.js --network sepolia
```

### Step 3: Copy Contract Address
After deployment, copy the contract address from the output.

### Step 4: Update Oracle Service Configuration
Update your environment variables:

```bash
# For Oracle Service
CONTRACT_ADDRESS=your_deployed_contract_address
RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
PRIVATE_KEY=your_private_key_here
ML_API_URL=http://localhost:5000
```

## 🧪 Testing on Sepolia

### 1. Start Your Services
```bash
# Start ML API
python src/app.py

# Start Web Interface
python src/web_interface.py

# Start Oracle Service (with Sepolia config)
python run_oracle_simple.py
```

### 2. Test the System
- Open: http://localhost:8081
- Enter test addresses
- Check blockchain data on Sepolia

## 🔍 Viewing on Sepolia

### Etherscan
- Go to: https://sepolia.etherscan.io/
- Search for your contract address
- View transactions and contract interactions

### Block Explorer
- Sepolia Block Explorer: https://sepolia.etherscan.io/
- View your contract: `https://sepolia.etherscan.io/address/YOUR_CONTRACT_ADDRESS`

## 💡 Tips

1. **Keep your private key secure** - Never share it
2. **Use testnet first** - Sepolia is for testing, not real money
3. **Monitor gas fees** - Sepolia gas fees are much lower than mainnet
4. **Backup your contract address** - You'll need it for your Oracle Service

## 🆘 Troubleshooting

### Common Issues:
1. **Insufficient Sepolia ETH** - Get more from faucet
2. **Invalid RPC URL** - Check your Infura/Alchemy URL
3. **Network issues** - Ensure you're connected to Sepolia
4. **Gas estimation failed** - Check contract code for errors

### Getting Help:
- Check Hardhat documentation
- Verify your environment variables
- Test with small amounts first
