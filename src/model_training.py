import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import os
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Define file paths
base_dir = "C:\\Users\\zainy\\Desktop\\Ethereum-Fraud-Detection-System"
data_dir = os.path.join(base_dir, "data")
input_filename = os.path.join(data_dir, "cleaned_data.csv")
results_dir = os.path.join(base_dir, "results")
model_filename = os.path.join(results_dir, "fraud_detection_model.joblib")

# Ensure the results directory exists
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

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
