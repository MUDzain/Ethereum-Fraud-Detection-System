# Ethereum Fraud Detection System

A comprehensive fraud detection system for Ethereum transactions using machine learning and blockchain analytics.

## Features

- 🔍 **Data Preprocessing**: Automated data cleaning and feature engineering
- 🤖 **Machine Learning Models**: Random Forest classifier with hyperparameter optimization
- 📊 **Model Evaluation**: Comprehensive performance analysis and visualizations
- ⚡ **High Performance**: Optimized models with 96% accuracy
- 🔒 **Feature Analysis**: Advanced feature importance analysis
- 📈 **Model Comparison**: Side-by-side evaluation of original vs optimized models
- 🌐 **Web API**: Flask-based REST API for real-time fraud detection
- 🔄 **Batch Processing**: Support for multiple address predictions

## Tech Stack

### Machine Learning
- **Python 3.8+** with pandas, numpy, scikit-learn
- **Random Forest Classifier** for fraud detection
- **GridSearchCV** for hyperparameter optimization
- **Matplotlib & Seaborn** for data visualization
- **Joblib** for model serialization

### Web API
- **Flask** for web framework
- **Flask-CORS** for cross-origin requests
- **JSON** for data exchange
- **RESTful API** design

### Data Processing
- **Pandas** for data manipulation and analysis
- **NumPy** for numerical computations
- **Scikit-learn** for machine learning pipeline

### Visualization
- **Matplotlib** for plotting and charts
- **Seaborn** for statistical visualizations
- **Confusion Matrix** and **Feature Importance** plots

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn joblib flask flask-cors
   ```

2. **Data Preprocessing**
   ```bash
   cd src
   python data_cleaning.py
   ```

3. **Train Basic Model**
   ```bash
   python model_training.py
   ```

4. **Hyperparameter Optimization**
   ```bash
   python hyperparameter_tuning.py
   ```

5. **Evaluate Models**
   ```bash
   python evaluate_tuned_model.py
   ```

6. **Start Web API**
   ```bash
   python app.py
   ```

## Project Structure

```
ethereum-fraud-detection-system/
├── data/                   # Dataset files
│   ├── transaction_dataset.csv    # Raw transaction data
│   └── cleaned_data.csv          # Processed data
├── src/                    # Source code
│   ├── data_cleaning.py           # Data preprocessing
│   ├── model_training.py          # Basic model training
│   ├── hyperparameter_tuning.py   # Model optimization
│   ├── evaluate_tuned_model.py    # Model comparison
│   ├── feature_importance_plot.py # Feature analysis
│   └── app.py                     # Flask web API
├── results/                # Output files
│   ├── fraud_detection_model.joblib      # Original model
│   ├── tuned_fraud_detection_model.joblib # Optimized model
│   ├── confusion_matrix.png              # Performance visualization
│   ├── feature_importance.png           # Feature analysis
│   └── model_comparison.png             # Model comparison
└── README.md              # Project documentation
```

## Web API

### API Endpoints

#### Health Check
```bash
GET http://localhost:5000/health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "Fraud Detection API is running"
}
```

#### Model Information
```bash
GET http://localhost:5000/model_info
```
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

#### Single Address Prediction
```bash
POST http://localhost:5000/predict
Content-Type: application/json

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

#### Batch Address Prediction
```bash
POST http://localhost:5000/batch_predict
Content-Type: application/json

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

### API Usage Examples

#### Using cURL
```bash
# Health check
curl http://localhost:5000/health

# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"address": "0x1234567890abcdef..."}'

# Batch prediction
curl -X POST http://localhost:5000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{"addresses": ["0x1234567890abcdef...", "0xfedcba0987654321..."]}'
```

#### Using Python
```python
import requests

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Single prediction
data = {'address': '0x1234567890abcdef...'}
response = requests.post('http://localhost:5000/predict', json=data)
result = response.json()
print(f"Fraud prediction: {result['prediction']}")
print(f"Probability: {result['probability']}")
```

## Model Performance

### Original Model
- **Accuracy**: 96%
- **Precision**: 96%
- **Recall**: 84%
- **F1-Score**: 90%

### Optimized Model (Hyperparameter Tuned)
- **Accuracy**: 96%
- **Precision**: 95%
- **Recall**: 86% ⬆️ **Improved**
- **F1-Score**: 90%

### Best Hyperparameters Found
- **n_estimators**: 200 (number of trees)
- **max_depth**: 20 (tree depth)
- **min_samples_split**: 5 (minimum samples to split)
- **min_samples_leaf**: 2 (minimum samples in leaf)

## Key Features

### Data Preprocessing
- Handles missing values
- Standardizes column names
- Removes duplicates
- Validates Ethereum addresses
- Feature engineering

### Model Training
- Random Forest Classifier
- Balanced class weights for imbalanced data
- Cross-validation for robust evaluation
- Feature importance analysis

### Hyperparameter Optimization
- GridSearchCV with 36 parameter combinations
- 3-fold cross-validation
- F1-score optimization
- Automated best parameter selection

### Model Evaluation
- Confusion matrix visualization
- Classification reports
- Feature importance comparison
- Performance metrics analysis

### Web API Features
- RESTful API design
- CORS support for cross-origin requests
- Error handling and validation
- Batch processing capabilities
- Real-time predictions

## Dataset Information

- **Size**: 9,841 Ethereum addresses
- **Features**: 47 numerical features
- **Fraud Rate**: 16.87% (1,660 fraud cases)
- **Features Include**:
  - Transaction patterns
  - Value statistics
  - Time-based features
  - ERC20 token interactions
  - Network behavior metrics

## Top 10 Most Important Features

1. **time_diff_between_first_and_last_(mins)** - 10.58%
2. **avg_val_received** - 8.20%
3. **total_ether_received** - 8.07%
4. **avg_min_between_received_tnx** - 6.57%
5. **max_value_received_** - 6.34%
6. **unique_received_from_addresses** - 5.77%
7. **total_ether_balance** - 5.18%
8. **_erc20_min_val_rec** - 5.16%
9. **total_ether_sent** - 4.87%
10. **min_value_received** - 4.40%

## Usage Examples

### Basic Model Training
```python
from src.model_training import train_and_evaluate_model
train_and_evaluate_model("data/cleaned_data.csv", "results/")
```

### Hyperparameter Tuning
```python
from src.hyperparameter_tuning import tune_and_save_model
tune_and_save_model("data/cleaned_data.csv", "results/tuned_model.joblib")
```

### Model Evaluation
```python
from src.evaluate_tuned_model import evaluate_tuned_model
evaluate_tuned_model()
```

### Web API
```python
# Start the API server
python src/app.py

# API will be available at http://localhost:5000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
