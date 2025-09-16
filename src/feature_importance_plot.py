import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import sys

# Add project root to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import RESULTS_DIR, CLEANED_DATA_PATH

results_dir = str(RESULTS_DIR)
model_filename = os.path.join(results_dir, "fraud_detection_model.joblib")
input_filename = str(CLEANED_DATA_PATH)

def plot_feature_importance():
    """
    Loads the trained model and creates a feature importance plot
    """
    print("Loading trained model...")
    try:
        model = joblib.load(model_filename)
    except FileNotFoundError:
        print(f"Error: Model file '{model_filename}' not found.")
        return
    
    print("Loading data to get feature names...")
    try:
        df = pd.read_csv(input_filename)
    except FileNotFoundError:
        print(f"Error: Data file '{input_filename}' not found.")
        return
    
    # Get feature names (same as in training)
    features = df.drop(columns=['full_address', 'is_fraud'])
    X = features.select_dtypes(include='number')
    
    # Get feature importance
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    top_15_features = feature_importances.nlargest(15)
    
    print("Creating feature importance plot...")
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Create horizontal bar plot
    bars = plt.barh(range(len(top_15_features)), top_15_features.values)
    
    # Customize the plot
    plt.yticks(range(len(top_15_features)), top_15_features.index)
    plt.xlabel('Feature Importance Score')
    plt.title('Top 15 Most Important Features for Fraud Detection')
    plt.gca().invert_yaxis()  # Invert y-axis to show highest importance at top
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.001, bar.get_y() + bar.get_height()/2, 
                f'{width:.3f}', ha='left', va='center', fontsize=9)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    plot_filename = os.path.join(results_dir, 'feature_importance.png')
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"Feature importance plot saved to: {plot_filename}")
    
    # Display top 10 features in console
    print("\nTop 15 Most Important Features:")
    print(top_15_features)
    
    # Do not show plot in headless environments

if __name__ == '__main__':
    plot_feature_importance()
