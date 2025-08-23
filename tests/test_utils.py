import unittest
import sys
import os
import re
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestUtils(unittest.TestCase):
    """Basic utility tests"""
    
    def test_ethereum_address_validation(self):
        """Test if ethereum addresses are valid"""
        # Valid addresses
        valid = [
            "0x1234567890123456789012345678901234567890",
            "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
        ]
        
        # Invalid addresses
        invalid = [
            "0x123",  # too short
            "invalid_address",
            "1234567890123456789012345678901234567890"  # no 0x
        ]
        
        for addr in valid:
            self.assertTrue(self.is_valid_address(addr))
        
        for addr in invalid:
            self.assertFalse(self.is_valid_address(addr))
    
    def is_valid_address(self, address):
        """Check if address looks like ethereum address"""
        if not isinstance(address, str):
            return False
        
        # Basic check - starts with 0x and has right length
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return False
        
        return True
    
    def test_json_validation(self):
        """Test json parsing"""
        good_json = '{"key": "value"}'
        bad_json = '{"key": value}'  # missing quotes
        
        self.assertTrue(self.is_valid_json(good_json))
        self.assertFalse(self.is_valid_json(bad_json))
    
    def is_valid_json(self, json_str):
        """Check if string is valid json"""
        try:
            json.loads(json_str)
            return True
        except:
            return False
    
    def test_number_validation(self):
        """Test number validation"""
        good_numbers = [1, 2.5, "123", "45.67"]
        bad_numbers = ["abc", "12a", None]
        
        for num in good_numbers:
            self.assertTrue(self.is_number(num))
        
        for num in bad_numbers:
            self.assertFalse(self.is_number(num))
    
    def is_number(self, value):
        """Check if value is a number"""
        if isinstance(value, (int, float)):
            return True
        
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        
        return False

if __name__ == '__main__':
    unittest.main()
