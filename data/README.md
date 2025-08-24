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

## Where the Data Came From

- **Ethereum blockchain data** I collected using Web3 APIs
- **Public transaction datasets** from academic research sources
- **Known fraud cases** and patterns I found in the literature
- **Real-time transaction monitoring** capabilities I built

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
- It has a good balance of legitimate and fraudulent addresses
- The features capture important transaction patterns
- It's large enough to train a reliable model
- The data quality is good with minimal missing values

This dataset forms the foundation for my machine learning model to detect fraudulent Ethereum addresses.
