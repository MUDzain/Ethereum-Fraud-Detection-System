# Deploying to Ethereum Sepolia Testnet

This guide explains how I deployed my Fraud Detection Smart Contract to the Ethereum Sepolia testnet.

## What You Need Before Starting

### 1. Get a Sepolia RPC URL
- **Infura** (what I used): https://infura.io/
  1. Create a free account
  2. Create a new project
  3. Copy the Sepolia endpoint URL
  4. Format: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`

- **Alchemy**: https://alchemy.com/
- **QuickNode**: https://quicknode.com/

### 2. Get Some Sepolia ETH
- **Sepolia Faucet**: https://sepoliafaucet.com/
- **Alchemy Faucet**: https://sepoliafaucet.com/
- You need about 0.1 Sepolia ETH for deployment

### 3. Get an Etherscan API Key
- Go to: https://etherscan.io/
- Create an account
- Get an API key from your profile

## Setting Up Environment Variables

Create a `.env` file in your project root:

```bash
# Sepolia Network Configuration
SEPOLIA_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
PRIVATE_KEY=your_private_key_here

# Etherscan API Key (for contract verification)
ETHERSCAN_API_KEY=your_etherscan_api_key_here
```

## Deployment Steps

### Step 1: Compile the Contracts
```bash
npx hardhat compile
```

### Step 2: Deploy to Sepolia
```bash
npx hardhat run scripts/deploy_sepolia.js --network sepolia
```

### Step 3: Copy the Contract Address
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

## Testing on Sepolia

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

## Viewing on Sepolia

### Etherscan
- Go to: https://sepolia.etherscan.io/
- Search for your contract address
- View transactions and contract interactions

### Block Explorer
- Sepolia Block Explorer: https://sepolia.etherscan.io/
- View your contract: `https://sepolia.etherscan.io/address/YOUR_CONTRACT_ADDRESS`

## Tips I Learned

1. **Keep your private key secure** - Never share it or commit it to git
2. **Use testnet first** - Sepolia is for testing, not real money
3. **Monitor gas fees** - Sepolia gas fees are much lower than mainnet
4. **Backup your contract address** - You'll need it for your Oracle Service

## Troubleshooting

### Common Issues I Encountered:
1. **Insufficient Sepolia ETH** - Get more from the faucet
2. **Invalid RPC URL** - Check your Infura/Alchemy URL format
3. **Network issues** - Make sure you're connected to Sepolia
4. **Gas estimation failed** - Check your contract code for errors

### Getting Help:
- Check Hardhat documentation
- Verify your environment variables are set correctly
- Test with small amounts first

## Why I Chose Sepolia

I deployed to Sepolia testnet because:
- It's free to use (no real ETH needed)
- It's the current standard testnet for Ethereum
- It has good tool support and documentation
- It's perfect for academic projects like this one

## My Deployment Experience

When I deployed my contract, I had to:
1. Set up an Infura account and get the RPC URL
2. Get some Sepolia ETH from the faucet
3. Configure the environment variables
4. Run the deployment script
5. Verify the contract on Etherscan

The deployment took about 5 minutes and cost less than 0.01 Sepolia ETH in gas fees.

## Contract Verification

After deployment, I verified my contract on Etherscan so others can see the source code and interact with it. This is important for transparency and trust.

This deployment process shows how blockchain technology can be used in real applications, even for academic projects.
