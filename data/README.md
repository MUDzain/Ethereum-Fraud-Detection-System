# Data Directory

This folder holds the data used by the project.

## What's here

- `transaction_dataset.csv` - Raw Ethereum transaction data (9,841 addresses)
- `cleaned_data.csv` - The processed and cleaned version of the data
- `README.md` - This documentation file

## About the dataset

### Raw data (transaction_dataset.csv)
- Size: 9,841 Ethereum wallet addresses
- Features: 47 numeric features per address
- Fraud rate: 22.1% (2,179 fraud cases)
- Format: CSV with address, transaction patterns, and a fraud flag

### Processed data (cleaned_data.csv)
- Cleaned version of the raw file
- Light feature engineering
- Missing values handled
- Duplicates removed
- Ethereum address format checked
- Fraud rate: 22.1% (2,179 out of 9,841)

Note: 22.1% means roughly 1 in 5 addresses are labeled as fraud.

## Where the data came from

- Public dataset downloaded locally



## Feature categories

47 features across these groups:
- Transaction patterns: frequency, timing, values
- Address interactions: unique senders/receivers, ERC20 interactions
- Value stats: min, max, mean, totals
- Time-based: gaps between transactions, first/last times
- Balance: current and historical

## File formats

- CSV: main transaction data
- JSON: configs or pattern definitions (if added)
- TXT: logs or analysis notes (if generated)

## How the data is processed

Steps:
1. Load CSV
2. Clean (missing values, duplicates)
3. Feature engineering
4. Address validation
5. Save cleaned file for training

## Why this dataset works

Chosen because:
- Enough fraud cases (22.1%) to learn useful patterns
- Features capture key transaction behavior
- Large enough for training
- Generally clean with few missing values

This dataset is the foundation for training the model.
