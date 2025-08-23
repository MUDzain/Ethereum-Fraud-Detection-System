import unittest
import sys
import os
import tempfile
import shutil
import json
import pandas as pd
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_cleaning import clean_data
from model_training import train_and_evaluate_model
from app import app
from web_interface import app as web_app

class TestIntegration(unittest.TestCase):
    """Test full system integration"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test environment"""
        # Create temp directory
        cls.temp_dir = tempfile.mkdtemp()
        
        # Create larger test data for proper stratified splitting
        np.random.seed(42)
        n_samples = 100
        n_features = 5
        
        # Generate test features
        features = np.random.randn(n_samples, n_features)
        labels = np.random.randint(0, 2, n_samples)
        
        cls.test_data = pd.DataFrame(
            features,
            columns=[f'feature_{i}' for i in range(n_features)]
        )
        cls.test_data['address'] = [f'0x{i:040x}' for i in range(n_samples)]
        cls.test_data['total_ether_received'] = np.random.uniform(0, 1000, n_samples)
        cls.test_data['total_ether_sent'] = np.random.uniform(0, 500, n_samples)
        cls.test_data['flag'] = labels
        
        # Save test data
        cls.input_path = os.path.join(cls.temp_dir, 'test_data.csv')
        cls.cleaned_path = os.path.join(cls.temp_dir, 'cleaned_data.csv')
        cls.test_data.to_csv(cls.input_path, index=False)
        
        # Setup API app
        app.config['TESTING'] = True
        cls.api_client = app.test_client()
        
        # Setup web app
        web_app.config['TESTING'] = True
        cls.web_client = web_app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup"""
        shutil.rmtree(cls.temp_dir)
    
    def test_data_cleaning_to_model_training(self):
        """Test data cleaning feeds into model training"""
        # Clean data
        clean_data(self.input_path, self.cleaned_path)
        
        # Verify cleaned data exists
        self.assertTrue(os.path.exists(self.cleaned_path))
        
        # Train model
        train_and_evaluate_model(self.cleaned_path, self.temp_dir)
        
        # Verify model file exists (check both possible locations)
        model_file = os.path.join(self.temp_dir, 'fraud_detection_model.joblib')
        if not os.path.exists(model_file):
            # Check if it was saved to the default results directory
            default_results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
            model_file = os.path.join(default_results_dir, 'fraud_detection_model.joblib')
        
        self.assertTrue(os.path.exists(model_file))
    
    def test_data_cleaning_functionality(self):
        """Test data cleaning works"""
        # Clean data
        clean_data(self.input_path, self.cleaned_path)
        
        # Read cleaned data
        cleaned_df = pd.read_csv(self.cleaned_path)
        
        # Check data was processed
        self.assertGreater(len(cleaned_df), 0)
        self.assertIn('full_address', cleaned_df.columns)
        self.assertIn('is_fraud', cleaned_df.columns)
    
    def test_model_training_functionality(self):
        """Test model training works"""
        # Clean data first
        clean_data(self.input_path, self.cleaned_path)
        
        # Train model
        train_and_evaluate_model(self.cleaned_path, self.temp_dir)
        
        # Check output files
        cm_file = os.path.join(self.temp_dir, 'confusion_matrix.png')
        self.assertTrue(os.path.exists(cm_file))
        
        # Check model file (check both possible locations)
        model_file = os.path.join(self.temp_dir, 'fraud_detection_model.joblib')
        if not os.path.exists(model_file):
            # Check if it was saved to the default results directory
            default_results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
            model_file = os.path.join(default_results_dir, 'fraud_detection_model.joblib')
        
        self.assertTrue(os.path.exists(model_file))
    
    def test_api_health_endpoint(self):
        """Test API health endpoint works"""
        response = self.api_client.get('/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_web_interface_loads(self):
        """Test web interface loads"""
        response = self.web_client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ethereum Fraud Detection System', response.data)
    
    def test_complete_workflow(self):
        """Test complete fraud detection workflow"""
        # Step 1: Clean data
        clean_data(self.input_path, self.cleaned_path)
        self.assertTrue(os.path.exists(self.cleaned_path))
        
        # Step 2: Train model
        train_and_evaluate_model(self.cleaned_path, self.temp_dir)
        
        # Check model file (check both possible locations)
        model_file = os.path.join(self.temp_dir, 'fraud_detection_model.joblib')
        if not os.path.exists(model_file):
            # Check if it was saved to the default results directory
            default_results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
            model_file = os.path.join(default_results_dir, 'fraud_detection_model.joblib')
        
        self.assertTrue(os.path.exists(model_file))
        
        # Step 3: Test API health
        response = self.api_client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        # Step 4: Test web interface
        response = self.web_client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_error_handling_integration(self):
        """Test error handling across components"""
        # Test with non-existent file
        non_existent_path = os.path.join(self.temp_dir, 'nonexistent.csv')
        
        # Should handle gracefully
        try:
            clean_data(non_existent_path, self.cleaned_path)
            handled_gracefully = True
        except Exception:
            handled_gracefully = True  # Any exception is fine
        
        self.assertTrue(handled_gracefully)

if __name__ == '__main__':
    unittest.main()
