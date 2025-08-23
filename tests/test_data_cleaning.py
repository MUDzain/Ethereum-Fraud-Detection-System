import unittest
import pandas as pd
import numpy as np
import sys
import os
import tempfile

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_cleaning import clean_data

class TestDataCleaning(unittest.TestCase):
    """Test data cleaning functions"""
    
    def setUp(self):
        """Setup test data"""
        # Create temp directory
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test data
        self.test_data = pd.DataFrame({
            'address': ['0x123', '0x456', '0x789'],
            'total_ether_received': [100, 200, 300],
            'total_ether_sent': [50, 150, 250],
            'flag': [0, 1, 0]
        })
        
        # Save test data
        self.input_path = os.path.join(self.temp_dir, 'test_input.csv')
        self.output_path = os.path.join(self.temp_dir, 'test_output.csv')
        self.test_data.to_csv(self.input_path, index=False)
    
    def tearDown(self):
        """Clean up"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_clean_data_function_exists(self):
        """Test that clean_data function exists"""
        self.assertTrue(callable(clean_data))
    
    def test_clean_data_creates_output_file(self):
        """Test that clean_data creates output file"""
        clean_data(self.input_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
    
    def test_clean_data_handles_missing_values(self):
        """Test handling of missing values"""
        # Add some null values
        data_with_nulls = self.test_data.copy()
        data_with_nulls.loc[0, 'total_ether_received'] = np.nan
        
        # Save and clean
        data_with_nulls.to_csv(self.input_path, index=False)
        clean_data(self.input_path, self.output_path)
        
        # Check output exists
        self.assertTrue(os.path.exists(self.output_path))
    
    def test_clean_data_standardizes_columns(self):
        """Test column standardization"""
        clean_data(self.input_path, self.output_path)
        
        # Read cleaned data
        cleaned_df = pd.read_csv(self.output_path)
        
        # Check column names are lowercase
        for col in cleaned_df.columns:
            self.assertEqual(col, col.lower())
    
    def test_clean_data_removes_unnecessary_columns(self):
        """Test removal of unnecessary columns"""
        # Add unnecessary columns
        data_with_extra = self.test_data.copy()
        data_with_extra['Unnamed: 0'] = range(len(data_with_extra))
        data_with_extra['Index'] = range(len(data_with_extra))
        
        # Save and clean
        data_with_extra.to_csv(self.input_path, index=False)
        clean_data(self.input_path, self.output_path)
        
        # Read cleaned data
        cleaned_df = pd.read_csv(self.output_path)
        
        # Check unnecessary columns are removed
        self.assertNotIn('Unnamed: 0', cleaned_df.columns)
        self.assertNotIn('Index', cleaned_df.columns)

if __name__ == '__main__':
    unittest.main()
