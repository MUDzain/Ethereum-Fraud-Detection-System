# Data Directory

This directory contains all data files used for the Ethereum Fraud Detection System.

## Contents

- `transaction_dataset.csv` - Raw Ethereum transaction data (9,841 addresses)
- `cleaned_data.csv` - Processed and cleaned transaction data
- `README.md` - This documentation file

## Dataset Information

### Raw Data (`transaction_dataset.csv`)
- **Size**: 9,841 Ethereum wallet addresses
- **Features**: 47 numerical features per address
- **Fraud Rate**: 16.87% (1,660 fraud cases)
- **Format**: CSV with columns including address, transaction patterns, and fraud flag

### Processed Data (`cleaned_data.csv`)
- **Cleaned version** of the raw dataset
- **Feature engineering** applied
- **Missing values** handled
- **Duplicates** removed
- **Address validation** performed

## Data Sources

- **Ethereum blockchain data** via Web3 APIs
- **Public transaction datasets** from academic sources
- **Known fraud cases** and patterns
- **Real-time transaction monitoring** capabilities

## Feature Categories

The dataset includes 47 features across these categories:
- **Transaction patterns**: Frequency, timing, value distributions
- **Address interactions**: Unique senders/receivers, ERC20 interactions
- **Value statistics**: Min, max, average, total amounts
- **Time-based features**: Transaction intervals, first/last transaction times
- **Balance information**: Current and historical balances

## File Formats

- **CSV**: Transaction data and datasets
- **JSON**: Configuration and pattern files (if applicable)
- **TXT**: Log files and analysis results (if applicable)

## Data Processing

The data goes through several processing steps:
1. **Raw data loading** from CSV files
2. **Data cleaning** (handling missing values, duplicates)
3. **Feature engineering** (creating derived features)
4. **Address validation** (ensuring valid Ethereum addresses)
5. **Output generation** (cleaned dataset for model training)
