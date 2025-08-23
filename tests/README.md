# Testing Suite

This directory contains tests for the Ethereum Fraud Detection System.

## ✅ Current Status

**All tests are passing!** 🎉
- **43 tests run**
- **0 failures, 0 errors**
- **100% pass rate**

## Running Tests

### Run all tests
```bash
python -m unittest discover tests
```

### Run specific test file
```bash
python -m unittest tests.test_data_cleaning
python -m unittest tests.test_model_training
python -m unittest tests.test_api
```

### Run with verbose output
```bash
python -m unittest discover tests -v
```

### Run test runner script
```bash
python tests/run_tests.py
```

## Test Files

- **test_utils.py** - Tests for utility functions
- **test_data_cleaning.py** - Tests for data cleaning
- **test_model_training.py** - Tests for model training
- **test_api.py** - Tests for API endpoints
- **test_web_interface.py** - Tests for web interface
- **test_oracle_service.py** - Tests for oracle service
- **test_integration.py** - End-to-end integration tests

## Test Categories

### Unit Tests
- Individual function testing
- Component isolation
- Mock external dependencies

### Integration Tests
- Component interaction
- Data flow testing
- End-to-end workflows

### API Tests
- HTTP endpoint testing
- Request/response validation
- Error handling

## Test Coverage

The tests cover:
- Data cleaning and preprocessing
- Model training and prediction
- API functionality
- Web interface
- Oracle service
- Complete system workflow

## Real Outputs Generated

When tests run, they generate:
- **Trained models** (`results/fraud_detection_model.joblib`)
- **Performance visualizations** (`results/confusion_matrix.png`)
- **Feature importance charts** (`results/feature_importance.png`)
- **Model comparison plots** (`results/model_comparison.png`)

## Writing Tests

### Basic Test Structure
```python
import unittest

class TestMyFunction(unittest.TestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_something(self):
        # Test logic here
        self.assertEqual(result, expected)
```

### Best Practices
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Clean up after tests

## Common Issues

### Import Errors
Make sure the src directory is in your Python path:
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
```

### Missing Dependencies
Install required packages:
```bash
pip install -r requirements.txt
```

### Model File Issues
Tests create temporary model files. Make sure you have write permissions in the test directory.

## Test Results

Tests should show:
- Number of tests run
- Number of failures/errors
- Test execution time

Example output:
```
Ran 43 tests in 41.68s
OK
```

## Recent Updates

- ✅ Fixed all import issues
- ✅ Updated tests to match actual implementations
- ✅ Increased test data size for proper model training
- ✅ All tests now pass successfully
- ✅ Real machine learning models are trained during testing
