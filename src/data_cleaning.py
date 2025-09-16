import pandas as pd
import os
import sys

# Add project root to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import TRANSACTION_DATASET_PATH, CLEANED_DATA_PATH, ensure_directories

def clean_data(input_path, output_path):
    """
    Cleans the transaction dataset by handling missing values and standardizing columns.
    """
    print(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        return
    
    print("Initial data shape:", df.shape)

    # Step 1: Drop unnecessary columns
    df = df.drop(columns=['Unnamed: 0', 'Index'], errors='ignore')
    print("Shape after dropping unnecessary columns:", df.shape)

    # Step 2: Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False)
    
    # Rename columns for clarity
    df = df.rename(columns={
        'address': 'full_address',
        'flag': 'is_fraud',
        'total_erc20_tnxs': 'total_erc20_transactions'
    }, errors='ignore')
    
    print("Standardized column names.")
    
    # Step 3: Handle missing values
    numerical_cols = df.select_dtypes(include=['number']).columns
    object_cols = df.select_dtypes(include=['object']).columns

    df[numerical_cols] = df[numerical_cols].fillna(0)
    df[object_cols] = df[object_cols].fillna('Unknown')
    
    print("Missing values filled.")
    
    # Step 4: Save the cleaned data to a new CSV file
    df.to_csv(output_path, index=False)
    print(f"\nSuccessfully saved cleaned data to {output_path}")

if __name__ == '__main__':
    ensure_directories()
    clean_data(str(TRANSACTION_DATASET_PATH), str(CLEANED_DATA_PATH))
