import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from oracle_service import FraudDetectionOracle

class TestOracleService(unittest.TestCase):
    """Test oracle service"""
    
    def setUp(self):
        """Setup test data"""
        self.oracle = FraudDetectionOracle()
        self.test_address = "0x1234567890123456789012345678901234567890"
    
    def test_oracle_init(self):
        """Test oracle initialization"""
        self.assertIsNotNone(self.oracle)
        self.assertTrue(hasattr(self.oracle, 'w3'))
    
    @patch('oracle_service.Web3')
    def test_connect_to_ethereum(self, mock_web3):
        """Test connecting to ethereum"""
        # Mock web3 connection
        mock_web3_instance = Mock()
        mock_web3.HTTPProvider.return_value = Mock()
        mock_web3.Web3.return_value = mock_web3_instance
        mock_web3_instance.is_connected.return_value = True
        
        oracle = FraudDetectionOracle()
        self.assertTrue(hasattr(oracle, 'w3'))
    
    def test_get_ml_prediction_method_exists(self):
        """Test that get_ml_prediction method exists"""
        self.assertTrue(hasattr(self.oracle, 'get_ml_prediction'))
        self.assertTrue(callable(self.oracle.get_ml_prediction))
    
    @patch('oracle_service.requests.post')
    def test_get_ml_prediction_success(self, mock_post):
        """Test successful ML prediction"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "prediction": 1,
            "probability": 0.85
        }
        mock_post.return_value = mock_response
        
        result = self.oracle.get_ml_prediction(self.test_address)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["prediction"], 1)
        self.assertEqual(result["probability"], 0.85)
    
    @patch('oracle_service.requests.post')
    def test_get_ml_prediction_api_error(self, mock_post):
        """Test API error handling"""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_post.return_value = mock_response
        
        result = self.oracle.get_ml_prediction(self.test_address)
        
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)
    
    def test_oracle_has_api_url(self):
        """Test oracle has API URL configuration"""
        self.assertTrue(hasattr(self.oracle, 'api_url'))
        self.assertIsInstance(self.oracle.api_url, str)
    
    def test_oracle_has_rpc_url(self):
        """Test oracle has RPC URL configuration"""
        self.assertTrue(hasattr(self.oracle, 'rpc_url'))
        self.assertIsInstance(self.oracle.rpc_url, str)
    
    def test_oracle_has_contract_abi(self):
        """Test oracle has contract ABI"""
        self.assertTrue(hasattr(self.oracle, 'contract_abi'))
        self.assertIsInstance(self.oracle.contract_abi, list)

if __name__ == '__main__':
    unittest.main()
