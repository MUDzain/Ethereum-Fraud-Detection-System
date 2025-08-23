import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from oracle_service import OracleService

class TestOracleService(unittest.TestCase):
    """Test oracle service"""
    
    def setUp(self):
        """Setup test data"""
        self.oracle = OracleService()
        self.test_address = "0x1234567890123456789012345678901234567890"
    
    def test_oracle_init(self):
        """Test oracle initialization"""
        self.assertIsNotNone(self.oracle)
        self.assertTrue(hasattr(self.oracle, 'web3'))
    
    @patch('oracle_service.Web3')
    def test_connect_to_ethereum(self, mock_web3):
        """Test connecting to ethereum"""
        # Mock web3 connection
        mock_web3_instance = Mock()
        mock_web3.HTTPProvider.return_value = Mock()
        mock_web3.Web3.return_value = mock_web3_instance
        mock_web3_instance.is_connected.return_value = True
        
        oracle = OracleService()
        self.assertTrue(hasattr(oracle, 'web3'))
    
    def test_get_balance(self):
        """Test getting balance"""
        # Mock web3 response
        with patch.object(self.oracle, 'web3') as mock_web3:
            mock_web3.eth.get_balance.return_value = 1000000000000000000  # 1 ETH in wei
            
            balance = self.oracle.get_balance(self.test_address)
            
            self.assertIsInstance(balance, int)
            self.assertGreaterEqual(balance, 0)
    
    def test_get_transaction_count(self):
        """Test getting transaction count"""
        with patch.object(self.oracle, 'web3') as mock_web3:
            mock_web3.eth.get_transaction_count.return_value = 5
            
            count = self.oracle.get_transaction_count(self.test_address)
            
            self.assertIsInstance(count, int)
            self.assertGreaterEqual(count, 0)
    
    def test_get_transaction_history(self):
        """Test getting transaction history"""
        with patch.object(self.oracle, 'web3') as mock_web3:
            # Mock transaction data
            mock_tx = Mock()
            mock_tx.value = 1000000000000000000  # 1 ETH
            mock_tx.to = self.test_address
            mock_tx.from_address = "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
            
            mock_web3.eth.get_transaction.return_value = mock_tx
            
            history = self.oracle.get_transaction_history(self.test_address, 1)
            
            self.assertIsInstance(history, list)
    
    def test_validate_address(self):
        """Test address validation"""
        valid_address = "0x1234567890123456789012345678901234567890"
        invalid_address = "invalid_address"
        
        # Test valid address
        self.assertTrue(self.oracle.validate_address(valid_address))
        
        # Test invalid address
        self.assertFalse(self.oracle.validate_address(invalid_address))
    
    def test_get_block_info(self):
        """Test getting block info"""
        with patch.object(self.oracle, 'web3') as mock_web3:
            # Mock block data
            mock_block = Mock()
            mock_block.number = 12345
            mock_block.timestamp = 1234567890
            
            mock_web3.eth.get_block.return_value = mock_block
            
            block_info = self.oracle.get_block_info(12345)
            
            self.assertIsInstance(block_info, dict)
            self.assertIn('number', block_info)
            self.assertIn('timestamp', block_info)

if __name__ == '__main__':
    unittest.main()
