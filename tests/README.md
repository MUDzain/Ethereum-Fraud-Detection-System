# Testing Suite

This directory contains all the tests for my Ethereum Fraud Detection System project.

## Current Status

All tests are working and passing:
- 43 tests total
- 0 failures, 0 errors
- 100% pass rate

## How to Run Tests

### Run all tests at once
```bash
python -m unittest discover tests
```

### Run specific test files
```bash
python -m unittest tests.test_data_cleaning
python -m unittest tests.test_model_training
python -m unittest tests.test_api
```

### Run with detailed output
```bash
python -m unittest discover tests -v
```

### Use the test runner script
```bash
python tests/run_tests.py
```

## Test Files Overview

- **test_utils.py** - Tests for helper functions
- **test_data_cleaning.py** - Tests for data preprocessing
- **test_model_training.py** - Tests for machine learning model
- **test_api.py** - Tests for the Flask API
- **test_web_interface.py** - Tests for the web interface
- **test_oracle_service.py** - Tests for blockchain oracle
- **test_integration.py** - Tests for the complete workflow

## Types of Tests

### Unit Tests
These test individual functions and components in isolation. I use mocks for external dependencies like API calls and blockchain interactions.

### Integration Tests
These test how different parts work together, like the data flow from cleaning to model training to prediction.

### API Tests
These test the Flask API endpoints to make sure they return the right responses and handle errors properly.

## What the Tests Cover

The test suite covers:
- Data cleaning and preprocessing functions
- Model training and prediction
- API functionality and endpoints
- Web interface components
- Oracle service for blockchain
- Complete system workflow from start to finish

## Outputs Generated During Testing

When you run the tests, they actually create:
- Trained ML models (saved to results/fraud_detection_model.joblib)
- Performance plots (confusion_matrix.png)
- Feature importance charts (feature_importance.png)
- Model comparison plots (model_comparison.png)

This means the tests are doing real work, not just checking if functions exist.

## How I Write Tests

### Basic Structure
```python
import unittest

class TestMyFunction(unittest.TestCase):
    def setUp(self):
        # Set up test data here
        pass
    
    def test_something(self):
        # Write the actual test here
        self.assertEqual(result, expected)
```

### What I Try to Do
- Use clear, descriptive test names
- Test both success and failure cases
- Mock external dependencies to avoid network calls
- Clean up after tests to avoid leaving files around

## Common Problems and Solutions

### Import Errors
If you get import errors, make sure the src directory is in your Python path:
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
```

### Missing Packages
If tests fail because of missing packages:
```bash
pip install -r requirements.txt
```

### Model File Issues
The tests create temporary model files. Make sure you have write permissions in the test directory.

## What Test Results Look Like

When tests run successfully, you should see something like:
```
Ran 43 tests in 41.68s
OK
```

## Recent Fixes I Made

- Fixed import issues that were causing tests to fail
- Updated tests to match the actual function signatures in my code
- Increased test data size so the ML model can train properly
- Made sure all tests pass consistently
- Tests now actually train real ML models during execution

## Why Testing is Important

Testing helps me make sure:
- My code works as expected
- Changes don't break existing functionality
- The system works end-to-end
- All components integrate properly

For this academic project, having comprehensive tests shows that I understand software development best practices and can write reliable code.
