import unittest
import sys
import os
import pytest

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    is_valid_ethereum_address,
    is_valid_json,
    is_number,
    normalize_address,
    checksum_address,
    calculate_risk_score,
    format_prediction_result,
    validate_prediction_input
)

class TestUtils(unittest.TestCase):
    """Test utility functions from the utils module"""
    
    def test_ethereum_address_validation_valid_addresses(self):
        """Test validation of valid Ethereum addresses"""
        valid_addresses = [
            "0x1234567890123456789012345678901234567890",
            "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
            "0x0000000000000000000000000000000000000000",
            "0xffffffffffffffffffffffffffffffffffffffff"
        ]
        
        for address in valid_addresses:
            with self.subTest(address=address):
                self.assertTrue(is_valid_ethereum_address(address))
    
    def test_ethereum_address_validation_invalid_addresses(self):
        """Test validation of invalid Ethereum addresses"""
        invalid_addresses = [
            "0x123",  # too short
            "invalid_address",  # no 0x prefix
            "1234567890123456789012345678901234567890",  # no 0x prefix
            "0x123456789012345678901234567890123456789g",  # invalid character
            "",  # empty string
            None,  # None value
            123,  # non-string
            "0x123456789012345678901234567890123456789",  # too short
            "0x12345678901234567890123456789012345678901"  # too long
        ]
        
        for address in invalid_addresses:
            with self.subTest(address=address):
                self.assertFalse(is_valid_ethereum_address(address))
    
    def test_json_validation_valid_json(self):
        """Test validation of valid JSON strings"""
        valid_json_strings = [
            '{"key": "value"}',
            '{"number": 123}',
            '{"array": [1, 2, 3]}',
            '{"nested": {"key": "value"}}',
            '[]',
            '{}',
            '"simple string"',
            '123',
            'true',
            'false',
            'null'
        ]
        
        for json_str in valid_json_strings:
            with self.subTest(json_str=json_str):
                self.assertTrue(is_valid_json(json_str))
    
    def test_json_validation_invalid_json(self):
        """Test validation of invalid JSON strings"""
        invalid_json_strings = [
            '{"key": value}',  # missing quotes
            '{"key": "value"',  # missing closing brace
            '{key: "value"}',  # missing quotes around key
            '{"key": "value",}',  # trailing comma
            'undefined',
            'function() {}',
            '{"key": undefined}'
        ]
        
        for json_str in invalid_json_strings:
            with self.subTest(json_str=json_str):
                self.assertFalse(is_valid_json(json_str))
    
    def test_number_validation_valid_numbers(self):
        """Test validation of valid numbers"""
        valid_numbers = [
            1,  # integer
            2.5,  # float
            "123",  # string integer
            "45.67",  # string float
            "0",  # zero
            "-123",  # negative integer
            "-45.67"  # negative float
        ]
        
        for number in valid_numbers:
            with self.subTest(number=number):
                self.assertTrue(is_number(number))
    
    def test_number_validation_invalid_numbers(self):
        """Test validation of invalid numbers"""
        invalid_numbers = [
            "abc",  # non-numeric string
            "12a",  # mixed alphanumeric
            None,  # None value
            [],  # list
            {},  # dict
            "12.34.56",  # multiple decimal points
            ""  # empty string
        ]
        
        for number in invalid_numbers:
            with self.subTest(number=number):
                self.assertFalse(is_number(number))
    
    def test_normalize_address(self):
        """Test address normalization"""
        test_cases = [
            ("0x1234567890123456789012345678901234567890", "0x1234567890123456789012345678901234567890"),
            ("0xABCDEFABCDEFABCDEFABCDEFABCDEFABCDEFABCD", "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd")
        ]
        
        for input_addr, expected in test_cases:
            with self.subTest(address=input_addr):
                result = normalize_address(input_addr)
                self.assertEqual(result, expected)
    
    def test_normalize_address_invalid(self):
        """Test address normalization with invalid addresses"""
        invalid_addresses = ["0x123", "invalid", None, 123]
        
        for address in invalid_addresses:
            with self.subTest(address=address):
                with self.assertRaises(ValueError):
                    normalize_address(address)
    
    def test_checksum_address(self):
        """Test address checksumming"""
        # Test with a known checksum address
        address = "0x1234567890123456789012345678901234567890"
        checksummed = checksum_address(address)
        self.assertIsInstance(checksummed, str)
        self.assertTrue(checksummed.startswith("0x"))
        self.assertEqual(len(checksummed), 42)
    
    def test_checksum_address_invalid(self):
        """Test address checksumming with invalid addresses"""
        invalid_addresses = ["0x123", "invalid", None, 123]
        
        for address in invalid_addresses:
            with self.subTest(address=address):
                with self.assertRaises(ValueError):
                    checksum_address(address)
    
    def test_calculate_risk_score(self):
        """Test risk score calculation"""
        # Test basic calculation
        risk = calculate_risk_score(0.8, 5000, 0)
        self.assertIsInstance(risk, int)
        self.assertGreaterEqual(risk, 0)
        self.assertLessEqual(risk, 100)
        
        # Test with high confidence
        high_risk = calculate_risk_score(0.9, 1000, 5)
        self.assertGreater(high_risk, 50)
        
        # Test with low confidence
        low_risk = calculate_risk_score(0.1, 9000, 0)
        self.assertLess(low_risk, 50)
    
    def test_format_prediction_result(self):
        """Test prediction result formatting"""
        result = format_prediction_result("0x1234567890123456789012345678901234567890", 1, 0.85)
        
        self.assertIn("address", result)
        self.assertIn("prediction", result)
        self.assertIn("probability", result)
        self.assertIn("is_fraud", result)
        self.assertIn("confidence_level", result)
        
        self.assertEqual(result["prediction"], 1)
        self.assertEqual(result["probability"], 0.85)
        self.assertTrue(result["is_fraud"])
        self.assertEqual(result["confidence_level"], "high")
    
    def test_validate_prediction_input_valid(self):
        """Test validation of valid prediction input"""
        valid_input = {"address": "0x1234567890123456789012345678901234567890"}
        address, errors = validate_prediction_input(valid_input)
        
        self.assertEqual(address, "0x1234567890123456789012345678901234567890")
        self.assertEqual(len(errors), 0)
    
    def test_validate_prediction_input_invalid(self):
        """Test validation of invalid prediction input"""
        # Missing address
        invalid_input = {}
        address, errors = validate_prediction_input(invalid_input)
        self.assertIn("Address is required", errors)
        
        # Invalid address format
        invalid_input = {"address": "invalid"}
        address, errors = validate_prediction_input(invalid_input)
        self.assertIn("Invalid Ethereum address format", errors)
        
        # Non-string address
        invalid_input = {"address": 123}
        address, errors = validate_prediction_input(invalid_input)
        self.assertIn("Address must be a string", errors)
        
        # Non-dict input
        address, errors = validate_prediction_input("not a dict")
        self.assertIn("Input must be a JSON object", errors)

if __name__ == '__main__':
    unittest.main()
