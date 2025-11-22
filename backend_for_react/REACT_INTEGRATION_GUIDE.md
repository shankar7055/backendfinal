# React Frontend Integration Guide

This guide will help you integrate this backend with your existing React frontend.

## 📋 Step-by-Step Integration

### Step 1: Copy Backend to Your React Project

Copy the entire `backend_for_react` folder to your React project root:

```
your-react-project/
├── src/
├── public/
├── backend_for_react/    ← Copy this folder here
│   ├── app.py
│   ├── ai_modules.py
│   └── ...
├── package.json
└── ...
```

### Step 2: Set Up Backend

```bash
cd backend_for_react
pip install -r requirements.txt
python generate_mock_data.py
python web_scraper.py
```

### Step 3: Create API Service in React

Create a new file in your React project: `src/services/api.js`

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Call Error:', error);
    throw error;
  }
};

// API Service Functions
export const apiService = {
  // Get all customers
  getCustomers: () => apiCall('/customers'),
  
  // Get inventory/products
  getInventory: () => apiCall('/inventory'),
  
  // Get all purchases
  getPurchases: () => apiCall('/purchases'),
  
  // Get purchases by customer ID
  getPurchasesByCustomer: (customerId) => apiCall(`/purchases/${customerId}`),
  
  // Get invoice by purchase ID
  getInvoice: (purchaseId) => apiCall(`/invoice/${purchaseId}`),
  
  // Get financials
  getFinancials: () => apiCall('/financials'),
  
  // Get competitors data
  getCompetitors: () => apiCall('/competitors'),
  
  // Get loyalty rewards
  getLoyaltyRewards: () => apiCall('/loyalty/active-customers'),
  
  // Get store design
  getStoreDesign: () => apiCall('/store-design/current'),
  
  // AI Query
  sendAIQuery: (query) => apiCall('/ai/query', {
    method: 'POST',
    body: JSON.stringify({ query }),
  }),
};
```

### Step 4: Update Your React Components

Example component using the API:

```javascript
import React, { useState, useEffect } from 'react';
import { apiService } from './services/api';

function Dashboard() {
  const [customers, setCustomers] = useState([]);
  const [financials, setFinancials] = useState(null);
  const [loading, setLoading] = useState(true);
  const [aiResponse, setAiResponse] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [customersData, financialsData] = await Promise.all([
        apiService.getCustomers(),
        apiService.getFinancials(),
      ]);
      setCustomers(customersData);
      setFinancials(financialsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAIQuery = async (query) => {
    try {
      const response = await apiService.sendAIQuery(query);
      setAiResponse(response.response);
    } catch (error) {
      console.error('AI Query Error:', error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Dashboard</h1>
      
      <section>
        <h2>Financials</h2>
        {financials && (
          <div>
            <p>Total Revenue: ${financials.total_revenue}</p>
            <p>Net Profit: ${financials.net_profit}</p>
            <p>Total Sales: {financials.total_sales_count}</p>
          </div>
        )}
      </section>

      <section>
        <h2>Customers ({customers.length})</h2>
        <ul>
          {customers.map(customer => (
            <li key={customer.customer_id}>{customer.name}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>AI Assistant</h2>
        <button onClick={() => handleAIQuery('Show me financial reports')}>
          Get Financial Report
        </button>
        {aiResponse && <p>{JSON.stringify(aiResponse)}</p>}
      </section>
    </div>
  );
}

export default Dashboard;
```

### Step 5: Environment Configuration

Create a `.env` file in your React project root:

```env
REACT_APP_API_URL=http://localhost:5000
```

### Step 6: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend_for_react
python app.py
```

**Terminal 2 - React Frontend:**
```bash
npm start
```

## 🔄 API Endpoint Mapping

Map your existing React buttons/functions to these endpoints:

| Frontend Function | Backend Endpoint | Method |
|------------------|------------------|--------|
| Get Customers | `/customers` | GET |
| Get Products | `/inventory` | GET |
| Get Financials | `/financials` | GET |
| Get Purchases | `/purchases` | GET |
| Get Invoice | `/invoice/<purchase_id>` | GET |
| AI Query | `/ai/query` | POST |
| Loyalty Rewards | `/loyalty/active-customers` | GET |
| Competitor Data | `/competitors` | GET |
| Store Design | `/store-design/current` | GET |

## 🎯 Example: Mapping Existing Buttons

If your React app has buttons like:

```javascript
// Before (no backend)
const handleGetCustomers = () => {
  // Local data or mock
};

// After (with backend)
const handleGetCustomers = async () => {
  try {
    const customers = await apiService.getCustomers();
    setCustomers(customers);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

## 🐛 Troubleshooting

### CORS Errors
- Make sure the backend is running
- Check that CORS is enabled in `app.py`
- Verify the API URL in your React app matches the backend port

### Connection Refused
- Ensure backend is running on port 5000
- Check firewall settings
- Verify `REACT_APP_API_URL` in `.env`

### Data Not Loading
- Run `python generate_mock_data.py` in the backend folder
- Check browser console for errors
- Verify API endpoints are correct

## 📝 Next Steps

1. ✅ Copy backend folder to React project
2. ✅ Install backend dependencies
3. ✅ Create API service in React
4. ✅ Update components to use API
5. ✅ Test all endpoints
6. ✅ Deploy backend (if needed)

## 🚀 Production Deployment

For production, you'll need to:

1. Deploy backend to a server (Heroku, AWS, etc.)
2. Update `REACT_APP_API_URL` to production URL
3. Configure CORS for production domain
4. Set up environment variables securely

