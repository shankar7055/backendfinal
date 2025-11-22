# 🚀 Quick Start Guide

## For React Developers

### 1. Copy This Folder
Copy the entire `backend_for_react` folder to your React project root.

### 2. Install & Setup (One Time)
```bash
cd backend_for_react
pip install -r requirements.txt
python generate_mock_data.py
python web_scraper.py
```

### 3. Start Backend
```bash
python app.py
```
Backend runs on: `http://localhost:5000`

### 4. Use in React
```javascript
// In your React component
const response = await fetch('http://localhost:5000/customers');
const customers = await response.json();
```

## 📡 All Available Endpoints

```
GET  /customers
GET  /inventory
GET  /purchases
GET  /purchases/<customer_id>
GET  /invoice/<purchase_id>
GET  /financials
GET  /competitors
GET  /loyalty/active-customers
GET  /store-design/current
POST /ai/query
```

## 🔧 Example React Code

```javascript
// Fetch customers
const customers = await fetch('http://localhost:5000/customers').then(r => r.json());

// AI Query
const aiResponse = await fetch('http://localhost:5000/ai/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Show me financials' })
}).then(r => r.json());
```

## ✅ That's It!

See `REACT_INTEGRATION_GUIDE.md` for detailed examples.

