# Ethereum Fraud Detection System

A comprehensive real-time fraud detection system for Ethereum transactions using machine learning and blockchain analytics.

## Features

- 🔍 **Real-time Transaction Monitoring**: Monitor Ethereum transactions in real-time
- 🤖 **Machine Learning Models**: Advanced ML models for fraud detection
- 📊 **Interactive Dashboard**: Beautiful UI with charts and analytics
- ⚡ **High Performance**: Fast processing with WebSocket connections
- 🔒 **Security**: Secure API endpoints and data validation
- 📈 **Analytics**: Comprehensive fraud analytics and reporting

## Tech Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- Chart.js for data visualization
- WebSocket for real-time updates

### Backend
- Node.js with Express
- TypeScript for type safety
- WebSocket for real-time communication
- Machine learning models (TensorFlow.js)

### Blockchain Integration
- Web3.js for Ethereum interaction
- Ethers.js for transaction processing
- Infura/Alchemy for blockchain data

## Quick Start

1. **Install Dependencies**
   ```bash
   npm run install-all
   ```

2. **Set up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Project Structure

```
ethereum-fraud-detection-system/
├── client/                 # React frontend
├── server/                 # Node.js backend
├── ml-models/             # Machine learning models
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## API Endpoints

- `GET /api/transactions` - Get recent transactions
- `POST /api/analyze` - Analyze transaction for fraud
- `GET /api/statistics` - Get fraud statistics
- `WS /ws` - WebSocket for real-time updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
