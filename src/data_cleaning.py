import pandas as pd
import os

# --- YOU MUST EDIT THIS LINE WITH THE CORRECT FILE PATH ---
# Example: input_path = r"C:\Your\Correct\Path\to\the\file.csv"
input_path = r"C:\Users\zainy\Desktop\Ethereum-Fraud-Detection-System\data\transaction_dataset.csv"

output_path = r"C:\Users\zainy\Desktop\Ethereum-Fraud-Detection-System\data\cleaned_data.csv"

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
    clean_data(input_path, output_path)
