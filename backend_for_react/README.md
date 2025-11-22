# Backend API for React Frontend

This backend provides a Flask-based REST API for your React e-commerce frontend. It includes AI-powered features, inventory management, financial analytics, and more.

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to the backend folder
cd backend_for_react

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Generate Mock Data

```bash
# Generate sample data
python generate_mock_data.py

# Generate competitor data
python web_scraper.py
```

### 3. Set Environment Variables (Optional)

```bash
# For OpenAI AI features (optional - works without it too)
export OPENAI_API_KEY="your_openai_api_key_here"
```

### 4. Run the Backend Server

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`

## 📡 API Endpoints

### Core Data Endpoints

- `GET /` - Server status check
- `GET /customers` - Get all customers
- `GET /inventory` - Get all products/inventory
- `GET /purchases` - Get all purchases
- `GET /purchases/<customer_id>` - Get purchases for a specific customer
- `GET /invoice/<purchase_id>` - Get invoice details
- `GET /financials` - Get financial summary
- `GET /competitors` - Get competitor data
- `GET /loyalty/active-customers` - Get loyalty rewards for active customers
- `GET /store-design/current` - Get current store design preview

### AI Endpoints

- `POST /ai/query` - AI-powered query processing
  ```json
  {
    "query": "Show me financial reports"
  }
  ```

## 🔧 React Integration

### 1. Update Your React App's API Base URL

In your React app, create a config file or update your API calls:

```javascript
// config.js or api.js
const API_BASE_URL = 'http://localhost:5000';

// Example API call
export const fetchCustomers = async () => {
  const response = await fetch(`${API_BASE_URL}/customers`);
  return response.json();
};

export const sendAIQuery = async (query) => {
  const response = await fetch(`${API_BASE_URL}/ai/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  return response.json();
};
```

### 2. CORS Configuration

The backend already has CORS enabled for all origins. If you need to restrict it:

```python
# In app.py, change:
CORS(app, resources={r"/*": {"origins": "*"}})

# To:
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
```

### 3. Example React Component

```javascript
import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [customers, setCustomers] = useState([]);
  const [financials, setFinancials] = useState(null);

  useEffect(() => {
    // Fetch customers
    fetch('http://localhost:5000/customers')
      .then(res => res.json())
      .then(data => setCustomers(data));

    // Fetch financials
    fetch('http://localhost:5000/financials')
      .then(res => res.json())
      .then(data => setFinancials(data));
  }, []);

  const handleAIQuery = async (query) => {
    const response = await fetch('http://localhost:5000/ai/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await response.json();
    console.log(data.response);
  };

  return (
    <div>
      <h1>Dashboard</h1>
      {/* Your React components */}
    </div>
  );
}
```

## 📁 Project Structure

```
backend_for_react/
├── app.py                 # Main Flask application
├── ai_modules.py          # AI business logic modules
├── openai_assistant.py    # OpenAI integration
├── generate_mock_data.py  # Data generation script
├── web_scraper.py         # Competitor data scraper
├── requirements.txt       # Python dependencies
├── data/                  # Data directory
│   ├── data.json         # Main e-commerce data
│   └── competitor_data.json  # Competitor data
└── README.md             # This file
```

## 🔐 Environment Variables

Create a `.env` file (optional):

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_DEBUG=True
PORT=5000
```

## 🛠️ Features

- ✅ **Customer Management** - Track and manage customer data
- ✅ **Inventory Management** - Monitor product inventory and stock levels
- ✅ **Financial Analytics** - Real-time financial calculations and insights
- ✅ **AI-Powered Queries** - OpenAI integration for intelligent business queries
- ✅ **Purchase Tracking** - Complete purchase history and invoice generation
- ✅ **Competitor Analysis** - Web scraping and competitor data analysis
- ✅ **Loyalty Rewards** - Customer loyalty program management
- ✅ **Store Design** - AI-generated store design recommendations

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill

# Or change the port in app.py
port = int(os.environ.get('PORT', 5001))
```

### Data Not Found
```bash
# Regenerate data
python generate_mock_data.py
python web_scraper.py
```

### CORS Issues
Make sure CORS is enabled in `app.py`:
```python
CORS(app, resources={r"/*": {"origins": "*"}})
```

## 📝 Notes

- The backend works without OpenAI API key (uses fallback mode)
- All endpoints return JSON responses
- The backend is configured to work with React frontend on port 3000 (default)
- Mock data is generated automatically on first run

## 🚀 Deployment

For production deployment:

1. Set `FLASK_DEBUG=False`
2. Configure proper CORS origins
3. Use a production WSGI server (e.g., Gunicorn)
4. Set up environment variables securely
5. Use a reverse proxy (e.g., Nginx)

```bash
# Example with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

