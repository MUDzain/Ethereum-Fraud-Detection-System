import os
import sys
from pathlib import Path

# Set environment variables for blockchain connection
os.environ['CONTRACT_ADDRESS'] = "0x6ac1340cD2eA7F334D037466249196E16d1d0bda"
os.environ['PRIVATE_KEY'] = "40fa6923f260d746f7ef11feeab68cab558e22e088b0fe89642a5dddfaa13681"
os.environ['RPC_URL'] = "https://eth-sepolia.g.alchemy.com/v2/CJlM2xLQd6oOKAI2LcXoz"
os.environ['ML_API_URL'] = "http://localhost:5000"

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from oracle_service import main

if __name__ == "__main__":
    main()
