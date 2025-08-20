import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os
import joblib

base_dir = "C:\\Users\\zainy\\Desktop\\Ethereum-Fraud-Detection-System"
data_dir = os.path.join(base_dir, "data")
input_filename = os.path.join(data_dir, "cleaned_data.csv")
results_dir = os.path.join(base_dir, "results")
tuned_model_filename = os.path.join(results_dir, "tuned_fraud_detection_model.joblib")

if not os.path.exists(results_dir):
    os.makedirs(results_dir)

def tune_and_save_model(input_path, output_path):
    """
    Performs hyperparameter tuning on the RandomForestClassifier and saves the best model.
    """
    print(f"Loading cleaned data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        return
    
    print("Data loaded successfully. Preparing for hyperparameter tuning.")
    
    # Select only the numerical features, and drop the target column
    features = df.select_dtypes(include='number').drop(columns=['is_fraud'])
    target = df['is_fraud']

    X = features
    y = target
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Define the parameter grid to search
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    
    # Initialize the RandomForestClassifier with balanced class weights
    rf = RandomForestClassifier(random_state=42, class_weight='balanced')
    
    # Initialize GridSearchCV
    print("Starting hyperparameter search. This may take a few minutes...")
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2, scoring='f1')
    
    # Perform the grid search on the training data
    grid_search.fit(X_train, y_train)
    
    print("\nHyperparameter search complete.")
    
    # Get the best model and its parameters
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    
    print("\n--- Best Model Parameters ---")
    print(best_params)
    
    # Evaluate the best model on the test data
    print("\n--- Evaluation of the Best Model ---")
    y_pred = best_model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)
    
    joblib.dump(best_model, output_path)
    print(f"\nSuccessfully saved the tuned model to {output_path}")
    
if __name__ == '__main__':
    tune_and_save_model(input_filename, tuned_model_filename)
