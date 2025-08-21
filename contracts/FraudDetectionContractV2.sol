// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title FraudDetectionContractV2
 * @dev Smart contract for Ethereum fraud detection with ML integration
 * @author MUDzain
 */
contract FraudDetectionContractV2 {
    
    // Events
    event FraudAssessmentUpdated(
        address indexed walletAddress,
        bool hasMLPrediction,
        bool mlIsFraudulent,
        uint256 mlConfidence,
        uint256 timestamp,
        uint256 reputationScore,
        uint256 reportCount,
        uint256 overallRisk
    );
    
    event ReputationUpdated(
        address indexed walletAddress,
        uint256 oldScore,
        uint256 newScore,
        string reason
    );
    
    event OracleUpdated(address indexed oldOracle, address indexed newOracle);
    event OwnerUpdated(address indexed oldOwner, address indexed newOwner);
    
    // State variables
    address public owner;
    address public oracle;
    
    // Structs
    struct FraudAssessment {
        bool hasMLPrediction;
        bool mlIsFraudulent;
        uint256 mlConfidence;      // 0-10000 (basis points)
        uint256 mlTimestamp;
        uint256 reputationScore;   // 0-10000 (basis points)
        uint256 reportCount;
        uint256 overallRisk;       // 0-10000 (basis points)
    }
    
    // Mappings
    mapping(address => FraudAssessment) public fraudAssessments;
    mapping(address => uint256) public reputationScores;
    mapping(address => uint256) public reportCounts;
    mapping(address => bool) public isReported;
    
    // Constants
    uint256 public constant MAX_CONFIDENCE = 10000;
    uint256 public constant MAX_REPUTATION = 10000;
    uint256 public constant MAX_RISK = 10000;
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }
    
    modifier onlyOracle() {
        require(msg.sender == oracle, "Only oracle can call this function");
        _;
    }
    
    modifier onlyOwnerOrOracle() {
        require(msg.sender == owner || msg.sender == oracle, "Only owner or oracle can call this function");
        _;
    }
    
    /**
     * @dev Constructor
     * @param _oracle Address of the oracle service
     */
    constructor(address _oracle) {
        require(_oracle != address(0), "Oracle address cannot be zero");
        owner = msg.sender;
        oracle = _oracle;
        
        emit OracleUpdated(address(0), _oracle);
        emit OwnerUpdated(address(0), msg.sender);
    }
    
    /**
     * @dev Update fraud assessment from oracle
     * @param walletAddress Address to assess
     * @param hasMLPrediction Whether ML prediction exists
     * @param mlIsFraudulent Whether ML predicts fraud
     * @param mlConfidence ML confidence score (0-10000)
     * @param reputationScore Reputation score (0-10000)
     * @param reportCount Number of reports
     * @param overallRisk Overall risk score (0-10000)
     */
    function updateFraudAssessment(
        address walletAddress,
        bool hasMLPrediction,
        bool mlIsFraudulent,
        uint256 mlConfidence,
        uint256 reputationScore,
        uint256 reportCount,
        uint256 overallRisk
    ) external onlyOracle {
        require(walletAddress != address(0), "Invalid wallet address");
        require(mlConfidence <= MAX_CONFIDENCE, "Confidence exceeds maximum");
        require(reputationScore <= MAX_REPUTATION, "Reputation exceeds maximum");
        require(overallRisk <= MAX_RISK, "Risk exceeds maximum");
        
        // Update the assessment
        fraudAssessments[walletAddress] = FraudAssessment({
            hasMLPrediction: hasMLPrediction,
            mlIsFraudulent: mlIsFraudulent,
            mlConfidence: mlConfidence,
            mlTimestamp: block.timestamp,
            reputationScore: reputationScore,
            reportCount: reportCount,
            overallRisk: overallRisk
        });
        
        // Update reputation score
        reputationScores[walletAddress] = reputationScore;
        reportCounts[walletAddress] = reportCount;
        
        emit FraudAssessmentUpdated(
            walletAddress,
            hasMLPrediction,
            mlIsFraudulent,
            mlConfidence,
            block.timestamp,
            reputationScore,
            reportCount,
            overallRisk
        );
    }
    
    /**
     * @dev Get fraud assessment for an address
     * @param walletAddress Address to check
     * @return assessment Fraud assessment struct
     */
    function getFraudAssessment(address walletAddress) external view returns (FraudAssessment memory) {
        return fraudAssessments[walletAddress];
    }
    
    /**
     * @dev Get reputation score for an address
     * @param walletAddress Address to check
     * @return Reputation score (0-10000)
     */
    function getReputation(address walletAddress) external view returns (uint256) {
        return reputationScores[walletAddress];
    }
    
    /**
     * @dev Get report count for an address
     * @param walletAddress Address to check
     * @return Number of reports
     */
    function getReportCount(address walletAddress) external view returns (uint256) {
        return reportCounts[walletAddress];
    }
    
    /**
     * @dev Check if address has been reported
     * @param walletAddress Address to check
     * @return Whether address has been reported
     */
    function isAddressReported(address walletAddress) external view returns (bool) {
        return isReported[walletAddress];
    }
    
    /**
     * @dev Report an address as potentially fraudulent
     * @param walletAddress Address to report
     * @param reason Reason for report
     */
    function reportAddress(address walletAddress, string memory reason) external {
        require(walletAddress != address(0), "Invalid wallet address");
        require(walletAddress != msg.sender, "Cannot report yourself");
        require(bytes(reason).length > 0, "Reason cannot be empty");
        
        // Increment report count
        reportCounts[walletAddress]++;
        isReported[walletAddress] = true;
        
        // Decrease reputation score (penalty for being reported)
        uint256 currentReputation = reputationScores[walletAddress];
        uint256 penalty = 1000; // 10% penalty
        uint256 newReputation = currentReputation > penalty ? currentReputation - penalty : 0;
        
        reputationScores[walletAddress] = newReputation;
        
        // Update fraud assessment
        FraudAssessment storage assessment = fraudAssessments[walletAddress];
        assessment.reportCount = reportCounts[walletAddress];
        assessment.reputationScore = newReputation;
        assessment.overallRisk = calculateOverallRisk(assessment);
        
        emit ReputationUpdated(walletAddress, currentReputation, newReputation, reason);
        emit FraudAssessmentUpdated(
            walletAddress,
            assessment.hasMLPrediction,
            assessment.mlIsFraudulent,
            assessment.mlConfidence,
            assessment.mlTimestamp,
            newReputation,
            reportCounts[walletAddress],
            assessment.overallRisk
        );
    }
    
    /**
     * @dev Calculate overall risk score
     * @param assessment Fraud assessment to calculate risk for
     * @return Overall risk score (0-10000)
     */
    function calculateOverallRisk(FraudAssessment memory assessment) internal pure returns (uint256) {
        uint256 risk = 0;
        
        // ML prediction weight: 40%
        if (assessment.hasMLPrediction && assessment.mlIsFraudulent) {
            risk += (assessment.mlConfidence * 40) / 100;
        }
        
        // Reputation weight: 30%
        risk += ((MAX_REPUTATION - assessment.reputationScore) * 30) / 100;
        
        // Report count weight: 30%
        uint256 reportRisk = assessment.reportCount > 10 ? MAX_RISK : (assessment.reportCount * 1000);
        risk += (reportRisk * 30) / 100;
        
        return risk > MAX_RISK ? MAX_RISK : risk;
    }
    
    /**
     * @dev Update oracle address (only owner)
     * @param newOracle New oracle address
     */
    function updateOracle(address newOracle) external onlyOwner {
        require(newOracle != address(0), "Oracle address cannot be zero");
        address oldOracle = oracle;
        oracle = newOracle;
        
        emit OracleUpdated(oldOracle, newOracle);
    }
    
    /**
     * @dev Transfer ownership (only owner)
     * @param newOwner New owner address
     */
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Owner address cannot be zero");
        address oldOwner = owner;
        owner = newOwner;
        
        emit OwnerUpdated(oldOwner, newOwner);
    }
    
    /**
     * @dev Emergency function to clear assessment (only owner)
     * @param walletAddress Address to clear
     */
    function clearAssessment(address walletAddress) external onlyOwner {
        delete fraudAssessments[walletAddress];
        delete reputationScores[walletAddress];
        delete reportCounts[walletAddress];
        delete isReported[walletAddress];
    }
    
    /**
     * @dev Get contract information
     * @return Contract owner, oracle, and total assessments
     */
    function getContractInfo() external view returns (address, address, uint256) {
        return (owner, oracle, address(this).balance);
    }
}
