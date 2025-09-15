import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import os
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
import joblib

import sys
# Add project root to path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import RESULTS_DIR, CLEANED_DATA_PATH, ensure_directories

# Ensure directories exist
ensure_directories()

# Use configuration for file paths
input_filename = str(CLEANED_DATA_PATH)
results_dir = str(RESULTS_DIR)
model_filename = os.path.join(results_dir, "fraud_detection_model.joblib")

def train_and_evaluate_model(input_path, results_path):
    """
    Trains a RandomForestClassifier model on the cleaned data, evaluates its performance,
    and saves the trained model to a file.
    """
    print(f"Loading cleaned data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        return
    
    print("Data loaded successfully. Initializing model training.")
    
    # Define features (X) and target (y)
    features = df.drop(columns=['full_address', 'is_fraud'])
    target = df['is_fraud']

    X = features.select_dtypes(include='number')
    y = target
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    print(f"Data split into {len(X_train)} training and {len(X_test)} testing samples.")
    
    # Initialize and train the RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    print("Training RandomForestClassifier...")
    model.fit(X_train, y_train)
    print("Model training complete.")
    
    # --- Evaluate Model Performance ---
    y_pred = model.predict(X_test)
    print("\n--- Model Evaluation ---")
    
    # Classification Report
    print("Classification Report:")
    report = classification_report(y_test, y_pred)
    print(report)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    # Visualize the Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Legitimate', 'Fraudulent'],
                yticklabels=['Legitimate', 'Fraudulent'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    
    confusion_matrix_path = os.path.join(results_path, 'confusion_matrix.png')
    plt.savefig(confusion_matrix_path)
    print(f"\nConfusion matrix saved to {confusion_matrix_path}")

    # Feature Importance
    print("\n--- Feature Importance ---")
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    top_10_features = feature_importances.nlargest(10)
    print("Top 10 most important features:")
    print(top_10_features)
    
    # --- Save the Trained Model ---
    joblib.dump(model, model_filename)
    print(f"\nSuccessfully saved the trained model to {model_filename}")
    
if __name__ == '__main__':
    train_and_evaluate_model(input_filename, results_dir)
