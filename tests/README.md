# Test Suite for Ethereum Fraud Detection System

This directory contains comprehensive tests for the Ethereum Fraud Detection System, designed to ensure the reliability and correctness of all system components.

## Overview

The test suite follows industry best practices and provides comprehensive coverage of:
- **Unit Tests**: Individual function and method testing
- **Integration Tests**: Component interaction testing  
- **API Tests**: REST endpoint functionality testing
- **Web Interface Tests**: User interface testing
- **Utility Tests**: Common utility function testing

## Test Structure

The test suite is organized into focused test modules:

### `test_api.py` - API Endpoint Tests
Tests for the Flask REST API endpoints:
- **Health Check**: `/health` endpoint functionality
- **Model Information**: `/model_info` endpoint data accuracy
- **Single Prediction**: `/predict` endpoint with various inputs
- **Batch Prediction**: `/batch_predict` endpoint for multiple addresses
- **Error Handling**: Invalid inputs, missing data, malformed requests
- **Content Type Validation**: Proper JSON handling
- **Edge Cases**: Empty requests, wrong content types

### `test_model_training.py` - Machine Learning Tests
Tests for the ML model training pipeline:
- **Model Creation**: Successful model training and file generation
- **File Outputs**: Confusion matrix, model artifacts, evaluation metrics
- **Data Processing**: Input data validation and preprocessing
- **Error Handling**: Missing files, invalid data formats
- **Model Persistence**: Model saving and loading functionality

### `test_web_interface.py` - Web Interface Tests
Tests for the user-facing web interface:
- **Page Loading**: Successful page rendering and HTTP responses
- **HTML Structure**: Proper document structure and semantic elements
- **Form Elements**: Input fields, submit buttons, validation attributes
- **Styling**: CSS presence and visual elements
- **JavaScript**: Client-side functionality and API integration
- **User Experience**: Results display, error handling, responsive design

### `test_integration.py` - System Integration Tests
End-to-end workflow testing:
- **Data Pipeline**: Raw data → cleaning → training → prediction
- **Service Integration**: API ↔ Web Interface ↔ Oracle communication
- **Component Interaction**: All services working together
- **Error Propagation**: Error handling across system boundaries
- **Performance**: System performance under various loads

### `test_utils.py` - Utility Function Tests
Tests for shared utility functions:
- **Address Validation**: Ethereum address format validation
- **JSON Validation**: JSON string parsing and validation
- **Number Validation**: Numeric value validation and conversion
- **Address Normalization**: Address formatting and checksumming
- **Risk Calculation**: Risk score computation algorithms
- **Input Validation**: Request data validation and sanitization

## Running Tests

### Prerequisites
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Using pytest (Recommended)
Pytest provides better test discovery, reporting, and debugging:

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run all tests with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run specific test class
pytest tests/test_api.py::TestAPI -v

# Run specific test method
pytest tests/test_api.py::TestAPI::test_health_endpoint -v

# Run tests matching a pattern
pytest tests/ -k "test_predict" -v

# Run tests with markers
pytest tests/ -m "unit" -v

# Run tests in parallel (if pytest-xdist installed)
pytest tests/ -n auto
```

### Using unittest (Alternative)
Traditional unittest framework:

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_api -v

# Run specific test class
python -m unittest tests.test_api.TestAPI -v

# Run specific test method
python -m unittest tests.test_api.TestAPI.test_health_endpoint -v
```

## Test Configuration

### pytest.ini Configuration
The project includes a `pytest.ini` file with:
- **Test Discovery**: Automatic test file and function discovery
- **Markers**: Custom markers for test categorization
- **Output Formatting**: Verbose output and colored results
- **Warning Filters**: Suppressed deprecation warnings

### Test Isolation
Each test maintains complete isolation:
- **Temporary Directories**: Unique temp directories per test
- **Mock Data**: Programmatically generated test data
- **Resource Cleanup**: Automatic cleanup after each test
- **No Shared State**: Tests don't depend on each other

### Test Data Management
- **Generated Data**: Tests create their own data to avoid external dependencies
- **Consistent Seeds**: Random seeds ensure reproducible results
- **Realistic Data**: Test data mimics real-world scenarios
- **Edge Cases**: Boundary conditions and error scenarios

## Test Categories and Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit`: Unit tests for individual functions
- `@pytest.mark.integration`: Integration tests for component interaction
- `@pytest.mark.api`: API endpoint tests
- `@pytest.mark.web`: Web interface tests
- `@pytest.mark.model`: Machine learning model tests
- `@pytest.mark.oracle`: Oracle service tests

## Continuous Integration

The test suite is designed for CI/CD pipelines:

### GitHub Actions Integration
```yaml
- name: Run Tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=src --cov-report=xml
```

### Docker Integration
```dockerfile
RUN pip install -r requirements.txt
RUN pytest tests/ --cov=src
```

### Performance Considerations
- **Fast Execution**: Full suite typically completes in under a minute
- **Minimal Dependencies**: No external services required
- **Parallel Execution**: Tests can run in parallel
- **Resource Efficient**: Minimal memory and CPU usage

## Adding New Tests

### Test Development Guidelines

1. **Naming Convention**: 
   - Files: `test_*.py`
   - Classes: `Test*`
   - Methods: `test_*`

2. **Test Structure**:
   ```python
   def test_functionality_under_condition(self):
       """Test description explaining what is being tested"""
       # Arrange: Set up test data and conditions
       # Act: Execute the functionality being tested
       # Assert: Verify the expected outcome
   ```

3. **Documentation**: Include comprehensive docstrings explaining:
   - What the test validates
   - Expected behavior
   - Edge cases covered

4. **Test Isolation**: Each test should:
   - Be independent of other tests
   - Clean up after itself
   - Use unique resources
   - Not modify global state

5. **Assertions**: Use specific assertions with clear failure messages:
   ```python
   self.assertEqual(actual, expected, "Clear failure message")
   self.assertIn(item, container, "Item should be in container")
   ```

### Example Test Template
```python
import unittest
import pytest

class TestNewFeature(unittest.TestCase):
    """Test suite for new feature functionality"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.test_data = create_test_data()
    
    def tearDown(self):
        """Clean up after each test"""
        cleanup_test_data()
    
    @pytest.mark.unit
    def test_feature_with_valid_input(self):
        """Test feature works correctly with valid input"""
        # Arrange
        input_data = self.test_data['valid']
        
        # Act
        result = feature_function(input_data)
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.value, expected_value)
    
    @pytest.mark.unit
    def test_feature_with_invalid_input(self):
        """Test feature handles invalid input gracefully"""
        # Arrange
        invalid_input = self.test_data['invalid']
        
        # Act & Assert
        with self.assertRaises(ValueError):
            feature_function(invalid_input)
```

## Test Coverage

### Coverage Goals
- **Line Coverage**: >90% of code lines executed
- **Branch Coverage**: >85% of conditional branches tested
- **Function Coverage**: 100% of public functions tested

### Coverage Reporting
```bash
# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html

# Generate XML coverage report for CI
pytest tests/ --cov=src --cov-report=xml

# View coverage summary
pytest tests/ --cov=src --cov-report=term-missing
```

## Troubleshooting

### Common Issues and Solutions

1. **Import Errors**
   ```bash
   # Ensure src directory is in Python path (bash/zsh)
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```
   PowerShell:
   ```powershell
   $env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)\src"
   ```

2. **File Permission Errors**
   ```bash
   # Ensure write permissions for temp directories
   chmod 755 /tmp
   ```

3. **Port Conflicts**
   - Tests use different ports than production
   - Check for running services on test ports
   - Use port checking utilities

4. **Test Failures**
   ```bash
   # Run with maximum verbosity
   pytest tests/ -vvv --tb=long
   
   # Run specific failing test
   pytest tests/test_specific.py::TestClass::test_method -vvv
   ```

### Debug Mode
```bash
# Run tests with debug output
pytest tests/ -v --log-cli-level=DEBUG

# Run single test with debugger
pytest tests/test_api.py::TestAPI::test_health_endpoint --pdb
```

### Performance Profiling
```bash
# Profile test execution time
pytest tests/ --durations=10

# Profile memory usage
pytest tests/ --profile
```

## Best Practices

### Test Quality
- **Single Responsibility**: Each test validates one specific behavior
- **Clear Intent**: Test names clearly describe what is being tested
- **Comprehensive Coverage**: Test both success and failure paths
- **Realistic Data**: Use data that reflects real-world usage

### Maintenance
- **Regular Updates**: Keep tests current with code changes
- **Refactoring**: Improve tests as the codebase evolves
- **Documentation**: Maintain clear documentation for complex tests
- **Performance**: Monitor and optimize test execution time

### Team Collaboration
- **Code Reviews**: Include test changes in code reviews
- **Shared Standards**: Follow consistent testing patterns
- **Knowledge Sharing**: Document testing strategies and decisions
- **Continuous Improvement**: Regularly evaluate and improve testing practices

## Current Test Status

- **Total Tests**: 62
- **Pass Rate**: 100% (all tests passing)
- **Coverage**: High coverage of critical functionality
- **Execution Time**: ~50 seconds on a typical laptop
- **Categories**: Unit, Integration, API, Web, Utility tests

## Outputs Generated During Testing

When you run the tests, they actually create:
- **Trained ML Models**: `results/fraud_detection_model.joblib`
- **Performance Plots**: `confusion_matrix.png`
- **Feature Importance**: `feature_importance.png`
- **Model Comparison**: `model_comparison.png`

This means the tests are doing real work, not just checking if functions exist.

## Why Testing is Important

Testing helps ensure:
- **Code Quality**: Functions work as expected
- **Regression Prevention**: Changes don't break existing functionality
- **System Reliability**: End-to-end workflows function correctly
- **Component Integration**: All parts work together properly
- **Documentation**: Tests serve as living documentation of expected behavior

For this academic project, having comprehensive tests demonstrates understanding of software development best practices and the ability to write reliable, maintainable code.