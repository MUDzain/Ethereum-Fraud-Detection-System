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

from data_cleaning import DataCleaner
from model_training import FraudDetectionModel
from app import app
from web_interface import app as web_app

class TestIntegration(unittest.TestCase):
    """Test full system integration"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test environment"""
        # Create temp directory
        cls.temp_dir = tempfile.mkdtemp()
        
        # Create test data
        cls.test_data = pd.DataFrame({
            'address': ['0x1234567890123456789012345678901234567890', 
                       '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd'],
            'total_ether_received': [100, 200],
            'total_ether_sent': [50, 150],
            'fraud': [0, 1]
        })
        
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
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_data(self.test_data)
        
        # Train model
        model = FraudDetectionModel()
        X = cleaned_data.drop(['address', 'fraud'], axis=1)
        y = cleaned_data['fraud']
        
        model.train(X, y)
        
        # Verify model was trained
        self.assertTrue(hasattr(model, 'model'))
        self.assertIsNotNone(model.model)
    
    def test_model_to_api_prediction(self):
        """Test model can make predictions via API"""
        # Train model
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_data(self.test_data)
        
        model = FraudDetectionModel()
        X = cleaned_data.drop(['address', 'fraud'], axis=1)
        y = cleaned_data['fraud']
        model.train(X, y)
        
        # Save model
        model_path = os.path.join(self.temp_dir, 'test_model.joblib')
        model.save_model(model_path)
        
        # Setup API with model
        app.config['MODEL_PATH'] = model_path
        
        # Test prediction
        test_address = "0x1234567890123456789012345678901234567890"
        response = self.api_client.post('/predict',
                                      data=json.dumps({'address': test_address}),
                                      content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('prediction', data)
    
    def test_api_to_web_interface(self):
        """Test API works with web interface"""
        # Train and save model
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_data(self.test_data)
        
        model = FraudDetectionModel()
        X = cleaned_data.drop(['address', 'fraud'], axis=1)
        y = cleaned_data['fraud']
        model.train(X, y)
        
        model_path = os.path.join(self.temp_dir, 'test_model.joblib')
        model.save_model(model_path)
        
        # Setup both apps
        app.config['MODEL_PATH'] = model_path
        web_app.config['MODEL_PATH'] = model_path
        
        # Test web interface loads
        response = self.web_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fraud Detection', response.data)
    
    def test_complete_workflow(self):
        """Test complete fraud detection workflow"""
        # Step 1: Clean data
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_data(self.test_data)
        
        # Step 2: Train model
        model = FraudDetectionModel()
        X = cleaned_data.drop(['address', 'fraud'], axis=1)
        y = cleaned_data['fraud']
        model.train(X, y)
        
        # Step 3: Save model
        model_path = os.path.join(self.temp_dir, 'workflow_model.joblib')
        model.save_model(model_path)
        
        # Step 4: Setup API
        app.config['MODEL_PATH'] = model_path
        
        # Step 5: Make prediction
        test_address = "0x1234567890123456789012345678901234567890"
        response = self.api_client.post('/predict',
                                      data=json.dumps({'address': test_address}),
                                      content_type='application/json')
        
        # Step 6: Verify result
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('prediction', data)
        self.assertIn('probability', data)
        self.assertEqual(data['address'], test_address)
    
    def test_error_handling_integration(self):
        """Test error handling across components"""
        # Test with invalid data
        invalid_data = pd.DataFrame({
            'address': ['invalid_address'],
            'total_ether_received': [100],
            'total_ether_sent': [50],
            'fraud': [0]
        })
        
        # Should handle gracefully
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_data(invalid_data)
        
        # Should filter out invalid addresses
        self.assertLess(len(cleaned_data), len(invalid_data))
    
    def test_model_persistence(self):
        """Test model can be saved and loaded"""
        # Train model
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_data(self.test_data)
        
        model = FraudDetectionModel()
        X = cleaned_data.drop(['address', 'fraud'], axis=1)
        y = cleaned_data['fraud']
        model.train(X, y)
        
        # Save model
        model_path = os.path.join(self.temp_dir, 'persist_model.joblib')
        model.save_model(model_path)
        
        # Load model
        loaded_model = FraudDetectionModel()
        loaded_model.load_model(model_path)
        
        # Test predictions match
        original_pred = model.predict(X.iloc[:2])
        loaded_pred = loaded_model.predict(X.iloc[:2])
        
        np.testing.assert_array_equal(original_pred, loaded_pred)

if __name__ == '__main__':
    unittest.main()
