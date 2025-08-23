import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_cleaning import DataCleaner

class TestDataCleaning(unittest.TestCase):
    """Test data cleaning functions"""
    
    def setUp(self):
        """Setup test data"""
        self.cleaner = DataCleaner()
        
        # Sample data for testing
        self.test_data = pd.DataFrame({
            'address': ['0x123', '0x456', '0x789'],
            'total_ether_received': [100, 200, 300],
            'total_ether_sent': [50, 150, 250],
            'fraud': [0, 1, 0]
        })
    
    def test_cleaner_init(self):
        """Test if cleaner initializes properly"""
        self.assertIsNotNone(self.cleaner)
        self.assertTrue(hasattr(self.cleaner, 'clean_data'))
    
    def test_clean_data_returns_df(self):
        """Test that clean_data returns a dataframe"""
        result = self.cleaner.clean_data(self.test_data)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_clean_data_keeps_columns(self):
        """Test that important columns are preserved"""
        result = self.cleaner.clean_data(self.test_data)
        self.assertIn('address', result.columns)
        self.assertIn('fraud', result.columns)
    
    def test_clean_data_handles_nulls(self):
        """Test handling of missing values"""
        # Add some null values
        data_with_nulls = self.test_data.copy()
        data_with_nulls.loc[0, 'total_ether_received'] = np.nan
        
        result = self.cleaner.clean_data(data_with_nulls)
        # Should handle nulls without crashing
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_clean_data_removes_duplicates(self):
        """Test duplicate removal"""
        # Add duplicate
        data_with_dupe = pd.concat([self.test_data, self.test_data.iloc[0:1]])
        
        result = self.cleaner.clean_data(data_with_dupe)
        # Should have same length as original
        self.assertEqual(len(result), len(self.test_data))
    
    def test_clean_data_bad_address(self):
        """Test with invalid address"""
        bad_data = self.test_data.copy()
        bad_data.loc[0, 'address'] = 'invalid_address'
        
        result = self.cleaner.clean_data(bad_data)
        # Should filter out bad addresses
        self.assertLess(len(result), len(bad_data))

if __name__ == '__main__':
    unittest.main()
