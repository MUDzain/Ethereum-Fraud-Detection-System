import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix

base_dir = "C:\\Users\\zainy\\Desktop\\Ethereum-Fraud-Detection-System"
results_dir = os.path.join(base_dir, "results")
data_dir = os.path.join(base_dir, "data")

# Model files
original_model_path = os.path.join(results_dir, "fraud_detection_model.joblib")
tuned_model_path = os.path.join(results_dir, "tuned_fraud_detection_model.joblib")
data_path = os.path.join(data_dir, "cleaned_data.csv")

def evaluate_tuned_model():
    """
    Evaluates the tuned model and compares it with the original model
    """
    print("Loading models and data...")
    
    # Load models
    try:
        original_model = joblib.load(original_model_path)
        tuned_model = joblib.load(tuned_model_path)
        print("Models loaded successfully!")
    except FileNotFoundError as e:
        print(f"Error loading model: {e}")
        return
    
    # Load data
    try:
        df = pd.read_csv(data_path)
        print("Data loaded successfully!")
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return
    
    # Prepare data
    features = df.select_dtypes(include='number').drop(columns=['is_fraud'])
    target = df['is_fraud']
    
    # Split data (same as training)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.3, random_state=42, stratify=target
    )
    
    print(f"Test set size: {len(X_test)} samples")
    
    # Evaluate both models
    print("\n" + "="*50)
    print("ORIGINAL MODEL EVALUATION")
    print("="*50)
    
    y_pred_original = original_model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred_original))
    
    print("\n" + "="*50)
    print("TUNED MODEL EVALUATION")
    print("="*50)
    
    y_pred_tuned = tuned_model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred_tuned))
    
    # Create comparison visualizations
    create_comparison_plots(y_test, y_pred_original, y_pred_tuned, original_model, tuned_model, X_test)
    
    # Feature importance comparison
    compare_feature_importance(original_model, tuned_model, X_test.columns)

def create_comparison_plots(y_test, y_pred_original, y_pred_tuned, original_model, tuned_model, X_test):
    """
    Creates comparison plots for both models
    """
    print("\nCreating comparison visualizations...")
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Original Model Confusion Matrix
    cm_original = confusion_matrix(y_test, y_pred_original)
    sns.heatmap(cm_original, annot=True, fmt='d', cmap='Blues', ax=axes[0,0])
    axes[0,0].set_title('Original Model - Confusion Matrix')
    axes[0,0].set_xlabel('Predicted')
    axes[0,0].set_ylabel('Actual')
    
    # Tuned Model Confusion Matrix
    cm_tuned = confusion_matrix(y_test, y_pred_tuned)
    sns.heatmap(cm_tuned, annot=True, fmt='d', cmap='Greens', ax=axes[0,1])
    axes[0,1].set_title('Tuned Model - Confusion Matrix')
    axes[0,1].set_xlabel('Predicted')
    axes[0,1].set_ylabel('Actual')
    
    # Feature Importance Comparison
    feature_importance_original = pd.Series(original_model.feature_importances_, index=X_test.columns)
    feature_importance_tuned = pd.Series(tuned_model.feature_importances_, index=X_test.columns)
    
    # Top 10 features comparison
    top_features = feature_importance_original.nlargest(10).index
    
    x = range(len(top_features))
    width = 0.35
    
    axes[1,0].bar([i - width/2 for i in x], feature_importance_original[top_features], width, label='Original', alpha=0.8)
    axes[1,0].bar([i + width/2 for i in x], feature_importance_tuned[top_features], width, label='Tuned', alpha=0.8)
    axes[1,0].set_xlabel('Features')
    axes[1,0].set_ylabel('Importance Score')
    axes[1,0].set_title('Feature Importance Comparison (Top 10)')
    axes[1,0].set_xticks(x)
    axes[1,0].set_xticklabels(top_features, rotation=45, ha='right')
    axes[1,0].legend()
    
    # Performance metrics comparison
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    
    metrics_original = {
        'Accuracy': accuracy_score(y_test, y_pred_original),
        'Precision': precision_score(y_test, y_pred_original),
        'Recall': recall_score(y_test, y_pred_original),
        'F1-Score': f1_score(y_test, y_pred_original)
    }
    
    metrics_tuned = {
        'Accuracy': accuracy_score(y_test, y_pred_tuned),
        'Precision': precision_score(y_test, y_pred_tuned),
        'Recall': recall_score(y_test, y_pred_tuned),
        'F1-Score': f1_score(y_test, y_pred_tuned)
    }
    
    metrics_df = pd.DataFrame({
        'Original': metrics_original,
        'Tuned': metrics_tuned
    })
    
    metrics_df.plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title('Performance Metrics Comparison')
    axes[1,1].set_ylabel('Score')
    axes[1,1].legend()
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save the comparison plot
    comparison_path = os.path.join(results_dir, 'model_comparison.png')
    plt.savefig(comparison_path, dpi=300, bbox_inches='tight')
    print(f"Model comparison plot saved to: {comparison_path}")
    
    plt.show()

def compare_feature_importance(original_model, tuned_model, feature_names):
    """
    Compares feature importance between original and tuned models
    """
    print("\n" + "="*50)
    print("FEATURE IMPORTANCE COMPARISON")
    print("="*50)
    
    # Get feature importance
    original_importance = pd.Series(original_model.feature_importances_, index=feature_names)
    tuned_importance = pd.Series(tuned_model.feature_importances_, index=feature_names)
    
    # Top 10 features for each model
    print("Top 10 Features - Original Model:")
    print(original_importance.nlargest(10))
    
    print("\nTop 10 Features - Tuned Model:")
    print(tuned_importance.nlargest(10))
    
    # Calculate correlation
    correlation = original_importance.corr(tuned_importance)
    print(f"\nFeature Importance Correlation: {correlation:.4f}")

if __name__ == '__main__':
    evaluate_tuned_model()
