import unittest
import sys
import os
import tempfile
import shutil

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from web_interface import app
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class TestWebInterface(unittest.TestCase):
    """Test web interface"""
    
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
    
    def test_home_page_loads(self):
        """Test home page loads"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ethereum Fraud Detection System', response.data)
        self.assertIn(b'Ethereum Wallet Address', response.data)
    
    def test_home_page_has_form(self):
        """Test page has form"""
        response = self.client.get('/')
        
        self.assertIn(b'<form', response.data)
        self.assertIn(b'input', response.data)
        self.assertIn(b'address', response.data)
    
    def test_home_page_has_button(self):
        """Test page has submit button"""
        response = self.client.get('/')
        
        self.assertIn(b'submit', response.data.lower())
        self.assertIn(b'check', response.data.lower())
    
    def test_home_page_has_css(self):
        """Test page has styling"""
        response = self.client.get('/')
        
        self.assertIn(b'<style>', response.data)
        self.assertIn(b'background', response.data)
    
    def test_home_page_has_js(self):
        """Test page has javascript"""
        response = self.client.get('/')
        
        self.assertIn(b'<script>', response.data)
        self.assertIn(b'fetch', response.data)
    
    def test_home_page_has_results_section(self):
        """Test page has results area"""
        response = self.client.get('/')
        
        self.assertIn(b'result', response.data)
        self.assertIn(b'prediction', response.data)
    
    def test_home_page_has_container(self):
        """Test page uses container layout"""
        response = self.client.get('/')
        
        self.assertIn(b'container', response.data)
    
    def test_home_page_html_structure(self):
        """Test proper HTML structure"""
        response = self.client.get('/')
        
        self.assertIn(b'<!DOCTYPE html>', response.data)
        self.assertIn(b'<html', response.data)
        self.assertIn(b'<head>', response.data)
        self.assertIn(b'<body>', response.data)

if __name__ == '__main__':
    unittest.main()
