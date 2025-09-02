# Data Directory

This directory contains all the data files I used for the Ethereum Fraud Detection System.

## What's in This Directory

- `transaction_dataset.csv` - Raw Ethereum transaction data (9,841 addresses)
- `cleaned_data.csv` - The processed and cleaned version of the data
- `README.md` - This documentation file

## About the Dataset

### Raw Data (transaction_dataset.csv)
- **Size**: 9,841 Ethereum wallet addresses
- **Features**: 47 numerical features for each address
- **Fraud Rate**: 22.1% (2,179 fraud cases)
- **Format**: CSV file with columns for address, transaction patterns, and fraud flag

### Processed Data (cleaned_data.csv)
- This is the cleaned version of the raw dataset
- I applied feature engineering to create better features
- Handled missing values by filling them appropriately
- Removed any duplicate entries
- Validated that all addresses are proper Ethereum addresses
- **Fraud Rate**: Still 22.1% (2,179 out of 9,841 addresses)

Note on the 22.1% fraud rate: This means roughly 1 in 5 addresses in the dataset
is labeled as fraudulent. That label distribution is not 50/50, so the dataset is
class-imbalanced. In practice, this affects metric selection and training strategy
(see notes below on how I handled it).

## Where the Data Came From

- Public dataset I downloaded locally

## A Note on Class Imbalance (22.1% Fraud)

- The dataset is imbalanced: 22.1% fraud vs 77.9% legitimate.
- Consequences: accuracy alone can be misleading; precision/recall and the
  confusion matrix are more informative.
- What I did to handle it:
  - Used a stratified train/test split so class ratios are preserved in both sets
  - Set `class_weight='balanced'` in the Random Forest during training
  - Reviewed precision/recall and the confusion matrix, not just accuracy

## Feature Categories

The dataset has 47 features across these main categories:
- **Transaction patterns**: How often transactions happen, timing patterns, value distributions
- **Address interactions**: How many unique senders/receivers, ERC20 token interactions
- **Value statistics**: Minimum, maximum, average, and total amounts
- **Time-based features**: Time between transactions, first and last transaction times
- **Balance information**: Current and historical balance data

## File Formats

- **CSV**: The main transaction data and datasets
- **JSON**: Configuration files and pattern definitions (if I add any)
- **TXT**: Log files and analysis results (if I generate any)

## How I Processed the Data

The data goes through several steps:
1. **Raw data loading** from CSV files
2. **Data cleaning** - handling missing values, removing duplicates
3. **Feature engineering** - creating new features from existing data
4. **Address validation** - making sure all addresses are valid Ethereum addresses
5. **Output generation** - saving the cleaned dataset for model training

## Why This Dataset Works Well

I chose this dataset because:
- It contains a meaningful number of fraudulent cases (22.1%), which is realistic
  for fraud problems yet sufficient for training
- The features capture important transaction patterns
- It's large enough to train a reliable model
- The data quality is good with minimal missing values

This dataset forms the foundation for my machine learning model to detect fraudulent Ethereum addresses.
