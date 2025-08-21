const { ethers } = require("hardhat");

async function main() {
    console.log("🚀 Deploying FraudDetectionContractV2...");

    // Get the contract factory
    const FraudDetectionContractV2 = await ethers.getContractFactory("FraudDetectionContractV2");
   
    // Get the deployer account
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
   
    // For now, we'll use the deployer as the oracle
    // In production, you'd use a separate oracle address
    const oracleAddress = deployer.address;
   
    // Deploy the contract
    const fraudDetectionContract = await FraudDetectionContractV2.deploy(oracleAddress);
    await fraudDetectionContract.waitForDeployment();

    const deployedAddress = await fraudDetectionContract.getAddress();
    console.log("✅ FraudDetectionContractV2 deployed to:", deployedAddress);
    console.log("🔗 Oracle address:", oracleAddress);
   
    // Verify the deployment
    console.log("\n📋 Contract Verification:");
    console.log("- Contract Address:", deployedAddress);
    console.log("- Owner:", await fraudDetectionContract.owner());
    console.log("- Oracle:", await fraudDetectionContract.oracle());
   
    // Test basic functionality
    console.log("\n🧪 Testing basic functionality...");
   
    // Test reputation score (should be 0 for new addresses)
    const testAddress = "0x0000000000000000000000000000000000000001";
    const reputation = await fraudDetectionContract.getReputation(testAddress);
    console.log("- Initial reputation for test address:", reputation.toString());
   
    // Test fraud assessment (should return default values)
    const assessment = await fraudDetectionContract.getFraudAssessment(testAddress);
    console.log("- Initial fraud assessment:", {
        hasMLPrediction: assessment[0],
        mlIsFraudulent: assessment[1],
        mlConfidence: assessment[2].toString(),
        mlTimestamp: assessment[3].toString(),
        reputationScore: assessment[4].toString(),
        reportCount: assessment[5].toString(),
        overallRisk: assessment[6].toString()
    });
   
    console.log("\n🎉 Deployment completed successfully!");
    console.log("\n📝 Next steps:");
    console.log("1. Update your oracle service with the contract address:", deployedAddress);
    console.log("2. Start your ML API server: python src/app.py");
    console.log("3. Run the oracle service: python src/oracle_service.py");
    console.log("4. Test the integration with real addresses");
   
    return deployedAddress;
}

// Handle errors
main()
    .then((address) => {
        console.log("\n✅ Deployment script completed");
        process.exit(0);
    })
    .catch((error) => {
        console.error("❌ Deployment failed:", error);
        process.exit(1);
    });
