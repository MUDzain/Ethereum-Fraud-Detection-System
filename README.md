# Ethereum Fraud Detection System

## Project Overview

This project implements a comprehensive fraud detection system for Ethereum blockchain transactions. The system combines machine learning algorithms with blockchain technology to identify fraudulent wallet addresses and store assessment results on-chain for transparency and immutability.

The project was developed as an academic examination project to demonstrate the integration of artificial intelligence with blockchain technology for real-world applications in cryptocurrency security.

## What This System Does

The Ethereum Fraud Detection System works by:

1. **Analyzing Transaction Patterns**: The system examines historical transaction data from Ethereum addresses to identify suspicious patterns
2. **Machine Learning Classification**: Using a Random Forest algorithm, it classifies addresses as either legitimate or fraudulent
3. **Real-time Assessment**: Provides instant fraud detection through a web interface and REST API
4. **Blockchain Storage**: Stores fraud assessment results on the Ethereum Sepolia testnet for permanent record
5. **Automated Updates**: An Oracle service continuously monitors and updates blockchain records

## Key Features

### Machine Learning Components
- **Advanced Data Preprocessing**: Automated cleaning and feature engineering of transaction data
- **Random Forest Classifier**: Trained on 9,841 Ethereum addresses with 47 features
- **Hyperparameter Optimization**: GridSearchCV optimization achieving 96% accuracy
- **Feature Importance Analysis**: Identifies the most critical transaction patterns for fraud detection
- **Model Performance Visualization**: Confusion matrices and comparison charts

### Web Application
- **Flask REST API**: Real-time fraud detection endpoints
- **Modern Web Interface**: User-friendly interface for address checking
- **Batch Processing**: Support for analyzing multiple addresses simultaneously
- **Responsive Design**: Works on desktop and mobile devices

### Blockchain Integration
- **Smart Contract**: Solidity contract deployed on Sepolia testnet
- **Oracle Service**: Automated bridge between ML predictions and blockchain
- **On-chain Storage**: Permanent storage of fraud assessments
- **Blockchain Viewer**: Command-line tool to inspect on-chain data

## Technology Stack

### Backend Technologies
- **Python 3.8+**: Core programming language
- **Pandas & NumPy**: Data manipulation and numerical computations
- **Scikit-learn**: Machine learning framework
- **Flask**: Web framework for API and interface
- **Web3.py**: Python library for Ethereum interaction

### Frontend Technologies
- **HTML5 & CSS3**: Web interface structure and styling
- **JavaScript**: Interactive functionality and API calls
- **Bootstrap**: Responsive design framework

### Blockchain Technologies
- **Solidity**: Smart contract programming language
- **Hardhat**: Ethereum development environment
- **Ethers.js**: JavaScript library for blockchain interaction
- **Sepolia Testnet**: Ethereum test network for deployment

### Data Visualization
- **Matplotlib**: Plotting and chart generation
- **Seaborn**: Statistical visualizations
- **Confusion Matrix**: Model performance evaluation

## Project Structure

```
ethereum-fraud-detection-system/
├── README.md                      # This file - project documentation
├── requirements.txt               # Python dependencies
├── package.json                   # Node.js dependencies
├── hardhat.config.js             # Hardhat configuration
├── .gitignore                    # Git ignore rules
├── start_services.py             # Service management utility
├── blockchain_viewer.py          # Blockchain data viewer
├── SEPOLIA_DEPLOYMENT.md         # Deployment guide
│
├── src/                          # Python source code
│   ├── app.py                    # Flask ML API server
│   ├── web_interface.py          # Web interface application
│   ├── oracle_service.py         # Oracle service for blockchain
│   ├── data_cleaning.py          # Data preprocessing
│   ├── model_training.py         # Basic model training
│   ├── hyperparameter_tuning.py  # Model optimization
│   ├── evaluate_tuned_model.py   # Model evaluation
│   └── feature_importance_plot.py # Feature analysis
│
├── contracts/                    # Smart contracts
│   ├── FraudDetectionContractV2.sol  # Main fraud detection contract
│   └── README.md                # Contract documentation
│
├── scripts/                      # Deployment scripts
│   ├── deploy_v2.js             # Local deployment
│   └── deploy_sepolia.js        # Sepolia deployment
│
├── data/                         # Dataset files
│   ├── transaction_dataset.csv   # Raw transaction data
│   ├── cleaned_data.csv         # Processed data
│   └── README.md                # Dataset documentation
│
└── results/                      # Model outputs
    ├── fraud_detection_model.joblib      # Original model
    ├── tuned_fraud_detection_model.joblib # Optimized model
    ├── confusion_matrix.png              # Performance visualization
    ├── feature_importance.png           # Feature analysis
    └── model_comparison.png             # Model comparison
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/MUDzain/Ethereum-Fraud-Detection-System.git
cd Ethereum-Fraud-Detection-System
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies
```bash
npm install
```

### Step 4: Data Preprocessing
```bash
cd src
python data_cleaning.py
```

### Step 5: Train the Machine Learning Model
```bash
python model_training.py
python hyperparameter_tuning.py
python evaluate_tuned_model.py
```

## Running the System

### Option 1: Start All Services (Recommended)
```bash
python start_services.py
```
This will start both the ML API and web interface simultaneously.

### Option 2: Start Services Individually

**Start the ML API:**
```bash
cd src
python app.py
```
The API will be available at `http://localhost:5000`

**Start the Web Interface:**
```bash
cd src
python web_interface.py
```
The web interface will be available at `http://localhost:8081`

### Option 3: Deploy Smart Contracts (Optional)
```bash
npx hardhat compile
npx hardhat run scripts/deploy_sepolia.js --network sepolia
```

### Option 4: Start Oracle Service (Optional)
```bash
python src/oracle_service.py
```

## How to Use the System

### Web Interface Usage
1. Open your browser and navigate to `http://localhost:8081`
2. Enter an Ethereum wallet address in the input field
3. Click "Check for Fraud" to analyze the address
4. View the results showing fraud prediction and confidence score

### API Usage
The system provides a REST API with the following endpoints:

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Single Address Prediction:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"address": "0x1234567890abcdef..."}'
```

**Batch Prediction:**
```bash
curl -X POST http://localhost:5000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{"addresses": ["0x1234567890abcdef...", "0xfedcba0987654321..."]}'
```

### Blockchain Viewer Usage
```bash
python blockchain_viewer.py
```
This tool allows you to view fraud assessments stored on the blockchain.

## Model Performance

The system achieves excellent performance metrics:

- **Accuracy**: 96%
- **Precision**: 95%
- **Recall**: 86%
- **F1-Score**: 90%

### Dataset Information
- **Total Addresses**: 9,841 Ethereum wallets
- **Features**: 47 numerical features
- **Fraud Rate**: 16.87% (1,660 fraud cases)
- **Feature Categories**: Transaction patterns, value statistics, time-based features, ERC20 interactions

### Top 10 Most Important Features
1. Time difference between first and last transaction (10.58%)
2. Average value received (8.20%)
3. Total ether received (8.07%)
4. Average minutes between received transactions (6.57%)
5. Maximum value received (6.34%)
6. Unique received from addresses (5.77%)
7. Total ether balance (5.18%)
8. ERC20 minimum value received (5.16%)
9. Total ether sent (4.87%)
10. Minimum value received (4.40%)

## Smart Contract Details

### Contract Address (Sepolia Testnet)
```
0x6ac1340cD2eA7F334D037466249196E16d1d0bda
```

### View on Etherscan
https://sepolia.etherscan.io/address/0x6ac1340cD2eA7F334D037466249196E16d1d0bda

### Contract Features
- **Fraud Assessment Storage**: Permanently store ML predictions
- **Reputation System**: Track wallet reputation scores
- **Report Management**: Handle user reports for suspicious addresses
- **Oracle Integration**: Automated updates from ML API
- **Access Control**: Owner and oracle role management

## API Documentation

### Endpoints

#### GET /health
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "message": "Fraud Detection API is running"
}
```

#### GET /model_info
Returns information about the trained model.

**Response:**
```json
{
  "model_type": "RandomForest",
  "feature_count": 47,
  "feature_names": [...],
  "dataset_size": 9841,
  "fraud_ratio": 0.1687
}
```

#### POST /predict
Analyzes a single Ethereum address for fraud.

**Request:**
```json
{
  "address": "0x1234567890abcdef..."
}
```

**Response:**
```json
{
  "address": "0x1234567890abcdef...",
  "prediction": 1,
  "probability": 0.85,
  "status": "success"
}
```

#### POST /batch_predict
Analyzes multiple Ethereum addresses for fraud.

**Request:**
```json
{
  "addresses": [
    "0x1234567890abcdef...",
    "0xfedcba0987654321..."
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "address": "0x1234567890abcdef...",
      "prediction": 1,
      "probability": 0.85
    },
    {
      "address": "0xfedcba0987654321...",
      "prediction": 0,
      "probability": 0.12
    }
  ],
  "status": "success"
}
```

## Development and Testing

### Running Tests
```bash
cd src
python -m pytest
```

### Code Quality
The project follows Python PEP 8 style guidelines and includes comprehensive error handling.

### Security Considerations
- Private keys are stored as environment variables
- Input validation on all API endpoints
- Secure blockchain transaction handling
- CORS protection for web interface

## Troubleshooting

### Common Issues

**ML API not starting:**
- Check if port 5000 is available
- Ensure all Python dependencies are installed
- Verify the model files exist in the results directory

**Web Interface not loading:**
- Ensure the ML API is running on port 5000
- Check if port 8081 is available
- Verify all dependencies are installed

**Blockchain connection issues:**
- Ensure Hardhat node is running (for local development)
- Check RPC URL configuration
- Verify contract address is correct

**Oracle Service errors:**
- Check ML API connectivity
- Verify blockchain network connection
- Ensure environment variables are set correctly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ethereum Foundation for blockchain technology
- Scikit-learn team for machine learning framework
- Flask team for web framework
- Hardhat team for Ethereum development tools

## Contact

For questions or support regarding this project, please refer to the GitHub repository issues section.

---

**Note**: This project is developed for academic purposes as part of an examination. The fraud detection model is trained on historical data and should be used for educational and research purposes only.
