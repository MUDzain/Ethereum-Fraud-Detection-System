const { ethers } = require("hardhat");

async function main() {
    console.log("🚀 Deploying FraudDetectionContractV2 to Sepolia Testnet...");
    
    // Get the deployer account
    const [deployer] = await ethers.getSigners();
    console.log("📝 Deploying contracts with account:", deployer.address);
    console.log("💰 Account balance:", (await ethers.provider.getBalance(deployer.address)).toString());

    // Deploy the contract
    const FraudDetectionContractV2 = await ethers.getContractFactory("FraudDetectionContractV2");
    
    // Use deployer as oracle for now (you can change this later)
    const oracleAddress = deployer.address;
    
    console.log("🔧 Deploying contract with oracle address:", oracleAddress);
    
    const fraudDetectionContract = await FraudDetectionContractV2.deploy(oracleAddress);
    await fraudDetectionContract.waitForDeployment();
    
    const deployedAddress = await fraudDetectionContract.getAddress();
    console.log("✅ FraudDetectionContractV2 deployed to:", deployedAddress);
    
    // Wait a bit for the transaction to be mined
    console.log("⏳ Waiting for deployment confirmation...");
    await new Promise(resolve => setTimeout(resolve, 10000));
    
    // Verify the deployment
    console.log("🔍 Verifying deployment...");
    try {
        const contractInfo = await fraudDetectionContract.getContractInfo();
        console.log("✅ Contract verification successful!");
        console.log("📊 Contract Info:");
        console.log("   - Owner:", contractInfo[0]);
        console.log("   - Oracle:", contractInfo[1]);
        console.log("   - Total Assessments:", contractInfo[2].toString());
    } catch (error) {
        console.log("❌ Contract verification failed:", error.message);
    }
    
    console.log("\n🎉 Deployment Complete!");
    console.log("📋 Next Steps:");
    console.log("1. Copy the contract address:", deployedAddress);
    console.log("2. Update your environment variables:");
    console.log("   CONTRACT_ADDRESS=" + deployedAddress);
    console.log("   RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID");
    console.log("   PRIVATE_KEY=your_private_key_here");
    console.log("3. Get some Sepolia ETH from: https://sepoliafaucet.com/");
    console.log("4. Test your contract on Sepolia!");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("❌ Deployment failed:", error);
        process.exit(1);
    });
