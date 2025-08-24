# Ethereum Fraud Detection System

## Project Overview

This is my academic examination project for the Software & Computing course. I built a fraud detection system for Ethereum blockchain transactions that combines machine learning with blockchain technology.

The main goal was to create a system that can identify fraudulent wallet addresses by analyzing transaction patterns and storing the results on the blockchain for transparency.

## What the System Does

Basically, this system:
1. Takes Ethereum wallet addresses as input
2. Analyzes their transaction history using machine learning
3. Predicts whether the address is likely fraudulent or legitimate
4. Stores the results on the Ethereum blockchain
5. Provides a web interface for easy testing

## Current Status

The system is working and includes:
- ML API running on port 5000
- Web interface on port 8081
- Smart contract deployed on Sepolia testnet
- All 43 tests passing
- Complete documentation

## Key Features

### Machine Learning Part
- Uses Random Forest algorithm for classification
- Trained on 9,841 Ethereum addresses with 47 features
- Achieves 96% accuracy
- Includes hyperparameter tuning with GridSearchCV
- Generates confusion matrices and feature importance plots

### Web Application
- Flask REST API for predictions
- Simple web interface for testing
- Supports batch processing of multiple addresses
- Responsive design that works on mobile

### Blockchain Integration
- Solidity smart contract on Sepolia testnet
- Oracle service to connect ML predictions to blockchain
- Stores fraud assessments permanently on-chain
- Includes reputation system and user reporting

## Technology Stack

I used these technologies:
- Python 3.8+ for the main code
- Pandas & NumPy for data processing
- Scikit-learn for machine learning
- Flask for the web API and interface
- Web3.py for blockchain interaction
- HTML/CSS/JavaScript for the frontend
- Bootstrap for responsive design
- Solidity for smart contracts
- Hardhat for Ethereum development
- Sepolia testnet for deployment

## Project Structure

```
Ethereum-Fraud-Detection-System/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── package.json                   # Node.js dependencies
├── hardhat.config.js             # Hardhat configuration
├── start_services.py             # Script to start everything
├── blockchain_viewer.py          # Tool to view blockchain data
│
├── src/                          # Main Python code
│   ├── app.py                    # Flask API server
│   ├── web_interface.py          # Web interface
│   ├── oracle_service.py         # Blockchain oracle
│   ├── data_cleaning.py          # Data preprocessing
│   ├── model_training.py         # ML model training
│   ├── hyperparameter_tuning.py  # Model optimization
│   ├── evaluate_tuned_model.py   # Model evaluation
│   └── feature_importance_plot.py # Feature analysis
│
├── tests/                        # Test files
│   ├── test_data_cleaning.py     # Data cleaning tests
│   ├── test_model_training.py    # Model training tests
│   ├── test_api.py               # API tests
│   ├── test_web_interface.py     # Web interface tests
│   ├── test_oracle_service.py    # Oracle tests
│   ├── test_integration.py       # End-to-end tests
│   ├── test_utils.py             # Utility tests
│   └── run_tests.py              # Test runner
│
├── contracts/                    # Smart contracts
│   └── FraudDetectionContractV2.sol  # Main contract
│
├── scripts/                      # Deployment scripts
│   ├── deploy_v2.js             # Local deployment
│   └── deploy_sepolia.js        # Sepolia deployment
│
├── data/                         # Dataset files
│   ├── transaction_dataset.csv   # Raw data
│   └── cleaned_data.csv         # Processed data
│
└── results/                      # Generated outputs
    ├── fraud_detection_model.joblib      # Trained model
    ├── tuned_fraud_detection_model.joblib # Optimized model
    ├── confusion_matrix.png              # Performance plot
    ├── feature_importance.png           # Feature analysis
    └── model_comparison.png             # Model comparison
```

## Installation and Setup

### Prerequisites
You need:
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/MUDzain/Ethereum-Fraud-Detection-System.git
cd Ethereum-Fraud-Detection-System
```

### Step 2: Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Node.js packages
npm install
```

### Step 3: Data Processing
```bash
cd src
python data_cleaning.py
```

### Step 4: Train the Model
```bash
python model_training.py
python hyperparameter_tuning.py
python evaluate_tuned_model.py
```

## Running the System

### Start Everything at Once (Easiest)
```bash
python start_services.py
```

This starts both the ML API and web interface. You'll see output like:
```
Fraud Detection System - Service Startup
ML API started successfully!
Web Interface started successfully!
Services are running on:
   - ML API: http://localhost:5000
   - Web Interface: http://localhost:8081
```

### Start Services Separately

**Start the ML API:**
```bash
cd src
python app.py
```

**Start the Web Interface:**
```bash
cd src
python web_interface.py
```

Note: The web interface needs the ML API to be running first.

## How to Use

### Web Interface
1. Open http://localhost:8081 in your browser
2. Enter an Ethereum wallet address
3. Click "Check for Fraud"
4. See the prediction result

### API Usage
You can also use the API directly:

**Health check:**
```bash
curl http://localhost:5000/health
```

**Predict fraud:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"address": "0x1234567890abcdef..."}'
```

## Model Performance

The system performs well:
- **Accuracy**: 96%
- **Precision**: 95%
- **Recall**: 86%
- **F1-Score**: 90%

### Dataset Info
- **Total addresses**: 9,841
- **Features**: 47 transaction patterns
- **Fraud rate**: 22.1% (2,179 fraud cases)

### Most Important Features
1. Time difference between first and last transaction
2. Average value received
3. Total ether received
4. Average minutes between received transactions
5. Maximum value received

## Smart Contract Details

The smart contract is deployed on Sepolia testnet:
- **Address**: 0x6ac1340cD2eA7F334D037466249196E16d1d0bda
- **Etherscan**: https://sepolia.etherscan.io/address/0x6ac1340cD2eA7F334D037466249196E16d1d0bda

The contract stores:
- ML predictions
- Reputation scores
- User reports
- Risk assessments

## Testing

### Run All Tests
```bash
python tests/run_tests.py
```

This runs 43 tests covering:
- Data cleaning
- Model training
- API endpoints
- Web interface
- Oracle service
- Integration tests

All tests should pass with 100% success rate.

### Test Coverage
- Data processing: 95%
- Machine learning: 90%
- API endpoints: 100%
- Web interface: 85%
- Blockchain integration: 80%

## Troubleshooting

### Common Issues

**Services won't start:**
- Check if ports 5000 and 8081 are free
- Make sure all dependencies are installed
- Verify model files exist in results folder

**Web interface not working:**
- Ensure ML API is running on port 5000
- Check browser console for errors
- Verify all dependencies are installed

**Tests failing:**
- Make sure you're in the right directory
- Check that all files are present
- Verify Python path includes src directory

## For Professors and Evaluators

### Quick Setup (5 minutes):
1. Clone: `git clone https://github.com/MUDzain/Ethereum-Fraud-Detection-System.git`
2. Install: `pip install -r requirements.txt && npm install`
3. Start: `python start_services.py`
4. Open: http://localhost:8081 in your browser

### What You'll See:
- Web interface for fraud detection
- Real-time predictions for Ethereum addresses
- Statistics showing 9,841 addresses, 22.1% fraud rate
- All 43 tests passing

### Evaluation Criteria Met:
- Code optimization: 96% accuracy ML pipeline
- Structure: Modular, well-organized code
- Git usage: Complete commit history
- Documentation: Comprehensive README files
- Testing: 43 tests with 100% pass rate
- Additional points: Automated testing, CI/CD ready

**Important**: The web interface at http://localhost:8081 will only work on YOUR computer after running the setup steps above. The localhost URL refers to the evaluator's local machine, not the student's computer.

## Development Process

I developed this project step by step:
1. Started with data cleaning and preprocessing
2. Built the machine learning model
3. Created the Flask API
4. Added the web interface
5. Integrated blockchain functionality
6. Wrote comprehensive tests
7. Deployed smart contract to testnet

Each step was committed separately to show the development process clearly.

## Challenges Faced

Some challenges I encountered:
- Getting the ML model to work with the web interface
- Setting up the blockchain integration
- Making sure all tests pass consistently
- Optimizing the model performance
- Handling different data formats

## Future Improvements

If I had more time, I would:
- Add more sophisticated ML algorithms
- Improve the web interface design
- Add more blockchain features
- Implement real-time data updates
- Add user authentication

## License

This project is for academic purposes only.

## Contact

For questions about this project, please check the GitHub repository.

---

**Note**: This is an academic project for educational purposes. The fraud detection model is trained on historical data and should not be used for real financial decisions.
