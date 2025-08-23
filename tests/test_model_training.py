import unittest
import pandas as pd
import numpy as np
import sys
import os
import tempfile
import shutil

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from model_training import FraudDetectionModel

class TestModelTraining(unittest.TestCase):
    """Test model training functions"""
    
    def setUp(self):
        """Setup test data"""
        self.model = FraudDetectionModel()
        
        # Create simple test data
        np.random.seed(42)
        n_samples = 50
        n_features = 5
        
        # Generate test features
        features = np.random.randn(n_samples, n_features)
        labels = np.random.randint(0, 2, n_samples)
        
        self.test_data = pd.DataFrame(
            features,
            columns=[f'feature_{i}' for i in range(n_features)]
        )
        self.test_data['fraud'] = labels
        self.test_data['address'] = [f'0x{i:040x}' for i in range(n_samples)]
        
        # Temp dir for model files
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)
    
    def test_model_init(self):
        """Test model initialization"""
        self.assertIsNotNone(self.model)
        self.assertTrue(hasattr(self.model, 'train'))
        self.assertTrue(hasattr(self.model, 'predict'))
    
    def test_model_training(self):
        """Test basic model training"""
        X = self.test_data.drop(['address', 'fraud'], axis=1)
        y = self.test_data['fraud']
        
        self.model.train(X, y)
        
        # Check model was trained
        self.assertTrue(hasattr(self.model, 'model'))
        self.assertIsNotNone(self.model.model)
    
    def test_model_prediction(self):
        """Test model predictions"""
        X = self.test_data.drop(['address', 'fraud'], axis=1)
        y = self.test_data['fraud']
        
        self.model.train(X, y)
        
        # Make predictions
        predictions = self.model.predict(X.iloc[:5])
        
        # Check predictions
        self.assertIsInstance(predictions, np.ndarray)
        self.assertEqual(len(predictions), 5)
        self.assertTrue(all(pred in [0, 1] for pred in predictions))
    
    def test_model_save_load(self):
        """Test saving and loading model"""
        X = self.test_data.drop(['address', 'fraud'], axis=1)
        y = self.test_data['fraud']
        
        self.model.train(X, y)
        
        # Save model
        model_path = os.path.join(self.temp_dir, 'test_model.joblib')
        self.model.save_model(model_path)
        
        # Check file exists
        self.assertTrue(os.path.exists(model_path))
        
        # Load model
        loaded_model = FraudDetectionModel()
        loaded_model.load_model(model_path)
        
        # Test predictions match
        original_pred = self.model.predict(X.iloc[:5])
        loaded_pred = loaded_model.predict(X.iloc[:5])
        
        np.testing.assert_array_equal(original_pred, loaded_pred)
    
    def test_model_evaluation(self):
        """Test model evaluation"""
        X = self.test_data.drop(['address', 'fraud'], axis=1)
        y = self.test_data['fraud']
        
        self.model.train(X, y)
        
        # Evaluate model
        metrics = self.model.evaluate(X, y)
        
        # Check metrics exist
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        
        # Check values are reasonable
        self.assertGreaterEqual(metrics['accuracy'], 0.0)
        self.assertLessEqual(metrics['accuracy'], 1.0)

if __name__ == '__main__':
    unittest.main()
