# E-Commerce AI Assistant - Backend API

A Flask-based backend API for an AI-powered e-commerce management system.

## Features

- **Customer Management** - Track and manage customer data
- **Inventory Management** - Monitor product inventory and stock levels
- **Financial Analytics** - Real-time financial calculations and insights
- **AI-Powered Queries** - OpenAI integration for intelligent business queries
- **Purchase Tracking** - Complete purchase history and invoice generation
- **Competitor Analysis** - Web scraping and competitor data analysis
- **Loyalty Rewards** - Customer loyalty program management
- **Store Design** - AI-generated store design recommendations

## Tech Stack

- **Python 3.8+**
- **Flask** - Web framework
- **OpenAI API** - AI-powered queries
- **Google Gemini** - Alternative AI provider (optional)
- **Pandas & NumPy** - Data processing
- **BeautifulSoup** - Web scraping

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shankar7055/backendfinal.git
   cd backendfinal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   # Optional: For Gemini features
   export GEMINI_API_KEY="your_gemini_api_key"
   ```

4. **Generate mock data** (if needed)
   ```bash
   python generate_mock_data.py
   python web_scraper.py
   ```

## Running the Server

```bash
python Backend_api1.py
```

The server will start on `http://localhost:5002` (or port specified in PORT environment variable).

## API Endpoints

### Core Endpoints
- `GET /` - Server status
- `GET /customers` - Get all customers
- `GET /inventory` - Get product inventory
- `GET /financials` - Get financial summary
- `GET /purchases` - Get all purchases
- `GET /purchases/<customer_id>` - Get customer purchases
- `GET /invoice/<purchase_id>` - Generate invoice

### AI & Advanced Features
- `POST /ai/query` - AI-powered business queries
- `GET /competitors` - Get competitor data
- `GET /loyalty/active-customers` - Get loyalty rewards
- `GET /store-design/current` - Get current store design

### Example API Call
```bash
# Get customers
curl http://localhost:5002/customers

# AI query
curl -X POST http://localhost:5002/ai/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me financial reports"}'
```

## Project Structure

```
backendfinal/
├── Backend_api1.py          # Main Flask application
├── ai_modules.py             # Core business logic
├── openai_assistant.py       # OpenAI integration
├── gemini_assistant.py       # Google Gemini integration (optional)
├── demo_mode.py              # Fallback demo mode
├── web_scraper.py            # Competitor data scraper
├── generate_mock_data.py     # Data generation script
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── data/                    # Data files (JSON)
    ├── data.json
    └── competitor_data.json
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - OpenAI API key (required for AI features)
- `GEMINI_API_KEY` - Google Gemini API key (optional)
- `PORT` - Server port (default: 5002)
- `FLASK_DEBUG` - Debug mode (default: False)

### Port Configuration
The default port is 5002 to avoid conflicts with macOS AirTunes on port 5000. You can change it by setting the `PORT` environment variable.

## Features

### AI Integration
- **OpenAI** - Primary AI provider for business queries
- **Google Gemini** - Alternative AI provider (optional)
- **Demo Mode** - Fallback when AI is unavailable

### Data Management
- JSON-based data storage
- Mock data generation
- Web scraping for competitor analysis

## Development

### Running Tests
```bash
python test_all_features.py
python test_all_connections.py
```

### Code Structure
- `Backend_api1.py` - Main Flask app with all routes
- `ai_modules.py` - Business logic and data processing
- `openai_assistant.py` - OpenAI API wrapper
- `gemini_assistant.py` - Gemini API wrapper

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.

