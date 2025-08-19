import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

def clean_data(input_path, output_path):
    """
    Clean and preprocess the transaction dataset
    
    Args:
        input_path (str): Path to the raw transaction dataset
        output_path (str): Path to save the cleaned dataset
    """
    print("🔄 Starting data cleaning process...")
    
    try:
        # Load the raw data
        print(f"📂 Loading data from {input_path}")
        df = pd.read_csv(input_path)
        print(f"📊 Original dataset shape: {df.shape}")
        
        # Remove unnecessary columns
        columns_to_drop = ['Unnamed: 0', 'Index']
        df = df.drop(columns=columns_to_drop, errors='ignore')
        
        # Standardize column names
        print("🔧 Standardizing column names...")
        df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False)
        
        # Rename specific columns for clarity
        column_mapping = {
            'address': 'full_address',
            'flag': 'is_fraud',
            'total_erc20_tnxs': 'total_erc20_transactions'
        }
        df = df.rename(columns=column_mapping, errors='ignore')
        
        # Handle missing values
        print("🔍 Handling missing values...")
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        # Convert boolean columns
        if 'is_fraud' in df.columns:
            df['is_fraud'] = df['is_fraud'].astype(bool)
        
        # Ensure address column is string
        if 'full_address' in df.columns:
            df['full_address'] = df['full_address'].astype(str)
        
        # Remove duplicates
        print("🧹 Removing duplicate addresses...")
        initial_count = len(df)
        df = df.drop_duplicates(subset=['full_address'], keep='first')
        final_count = len(df)
        print(f"Removed {initial_count - final_count} duplicate addresses")
        
        # Basic data validation
        print("✅ Performing data validation...")
        
        # Check for valid Ethereum addresses (basic format check)
        if 'full_address' in df.columns:
            valid_addresses = df['full_address'].str.match(r'^0x[a-fA-F0-9]{40}$')
            invalid_count = (~valid_addresses).sum()
            if invalid_count > 0:
                print(f"⚠️  Found {invalid_count} addresses with invalid format")
                df = df[valid_addresses]
        
        # Remove outliers from numeric columns (optional)
        print("📈 Removing extreme outliers...")
        for col in numeric_columns:
            if col != 'is_fraud':  # Don't process the target variable
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
                outlier_count = outliers.sum()
                if outlier_count > 0:
                    print(f"Removing {outlier_count} outliers from {col}")
                    df = df[~outliers]
        
        # Save cleaned data
        print(f"💾 Saving cleaned data to {output_path}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        
        # Print summary statistics
        print("\n📋 Data Cleaning Summary:")
        print(f"Final dataset shape: {df.shape}")
        print(f"Features: {len(df.columns) - 2}")  # Exclude address and target
        print(f"Addresses: {len(df)}")
        
        if 'is_fraud' in df.columns:
            fraud_count = df['is_fraud'].sum()
            fraud_percentage = (fraud_count / len(df)) * 100
            print(f"Fraud cases: {fraud_count} ({fraud_percentage:.2f}%)")
            print(f"Safe cases: {len(df) - fraud_count} ({100 - fraud_percentage:.2f}%)")
        
        print("✅ Data cleaning completed successfully!")
        return df
        
    except Exception as e:
        print(f"❌ Error during data cleaning: {str(e)}")
        raise

def create_sample_data(output_path, num_samples=1000):
    """
    Create sample data for testing when real data is not available
    
    Args:
        output_path (str): Path to save the sample dataset
        num_samples (int): Number of sample addresses to create
    """
    print("🔧 Creating sample dataset for testing...")
    
    # Generate sample Ethereum addresses
    import random
    import string
    
    def generate_ethereum_address():
        """Generate a random Ethereum address"""
        hex_chars = '0123456789abcdef'
        address = '0x' + ''.join(random.choice(hex_chars) for _ in range(40))
        return address
    
    # Create sample data
    data = []
    for i in range(num_samples):
        address = generate_ethereum_address()
        
        # Generate realistic transaction features
        total_transactions = random.randint(1, 1000)
        total_erc20_transactions = random.randint(0, total_transactions)
        total_eth_received = random.uniform(0, 1000)
        total_eth_sent = random.uniform(0, 1000)
        avg_transaction_value = random.uniform(0, 100)
        
        # Determine fraud based on some patterns
        is_fraud = False
        if (total_transactions > 500 and avg_transaction_value > 50) or \
           (total_erc20_transactions > total_transactions * 0.8) or \
           (total_eth_received > 500 and total_eth_sent < 10):
            is_fraud = random.random() < 0.7  # 70% chance of fraud for suspicious patterns
        
        data.append({
            'full_address': address,
            'total_transactions': total_transactions,
            'total_erc20_transactions': total_erc20_transactions,
            'total_eth_received': total_eth_received,
            'total_eth_sent': total_eth_sent,
            'avg_transaction_value': avg_transaction_value,
            'is_fraud': is_fraud
        })
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Sample dataset created with {len(df)} addresses")
    print(f"📁 Saved to: {output_path}")
    
    return df

if __name__ == "__main__":
    # Example usage
    input_file = "../data/transaction_dataset.csv"
    output_file = "../data/cleaned_data.csv"
    
    # Check if input file exists
    if os.path.exists(input_file):
        print("📂 Found transaction dataset, cleaning...")
        clean_data(input_file, output_file)
    else:
        print("📂 No transaction dataset found, creating sample data...")
        create_sample_data(output_file, num_samples=1000)
