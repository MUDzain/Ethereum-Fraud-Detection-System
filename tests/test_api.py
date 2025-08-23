import unittest
import json
import sys
import os
import tempfile
import shutil

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class TestAPI(unittest.TestCase):
    """Test API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test app"""
        # Create simple test model
        cls.temp_dir = tempfile.mkdtemp()
        cls.model_path = os.path.join(cls.temp_dir, 'test_model.joblib')
        
        # Make a basic model
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        X = np.random.randn(20, 5)
        y = np.random.randint(0, 2, 20)
        model.fit(X, y)
        
        # Save model
        joblib.dump(model, cls.model_path)
        
        # Setup app
        app.config['TESTING'] = True
        app.config['MODEL_PATH'] = cls.model_path
        cls.client = app.test_client()
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup"""
        shutil.rmtree(cls.temp_dir)
    
    def test_health_endpoint(self):
        """Test health check"""
        response = self.client.get('/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_model_info_endpoint(self):
        """Test model info"""
        response = self.client.get('/model_info')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('model_type', data)
        self.assertIn('feature_count', data)
    
    def test_predict_valid_address(self):
        """Test prediction with valid address"""
        test_address = "0x1234567890123456789012345678901234567890"
        
        response = self.client.post('/predict',
                                  data=json.dumps({'address': test_address}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('prediction', data)
        self.assertIn('probability', data)
        self.assertEqual(data['address'], test_address)
    
    def test_predict_invalid_address(self):
        """Test prediction with invalid address"""
        test_address = "invalid_address"
        
        response = self.client.post('/predict',
                                  data=json.dumps({'address': test_address}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_predict_missing_address(self):
        """Test prediction without address"""
        response = self.client.post('/predict',
                                  data=json.dumps({}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_batch_predict(self):
        """Test batch prediction"""
        test_addresses = [
            "0x1234567890123456789012345678901234567890",
            "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
        ]
        
        response = self.client.post('/batch_predict',
                                  data=json.dumps({'addresses': test_addresses}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 2)
    
    def test_nonexistent_endpoint(self):
        """Test 404 for bad endpoint"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
