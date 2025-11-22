# How to Run the Project

## Quick Start Guide

### Prerequisites Check
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check if dependencies are installed
python3 -c "import flask, pandas, openai; print('✅ Dependencies OK')"
```

---

## Option 1: Run Backend_api1.py (OpenAI-based) ⭐ Recommended

### Step 1: Set OpenAI API Key (Optional but Recommended)
```bash
export OPENAI_API_KEY="REDACTED_OPENAI_KEY3WfRbAALDeR816OT3BlbkFJA40H3MjYg9wkMCfxK2hIBTbZdY0wcU2UUk4Rf8KiZebnaEKlz2SVlcyNTqhRdU3L_eIbja6p0A"
```

### Step 2: Navigate to Project
```bash
cd /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub
```

### Step 3: Start the Server
```bash
python3 Backend_api1.py
```

You should see:
```
✅ MongoDB Connected Successfully
🚀 Server running on http://localhost:5000
```

### Step 4: Access the Application

**Option A: Use HTML Frontend**
- Open `index2.html` in your web browser
- Go to the "AI Assistant" tab
- Start using the application!

**Option B: Test API Directly**
```bash
# In another terminal, test endpoints:
curl http://localhost:5000/customers
curl http://localhost:5000/financials
curl -X POST http://localhost:5000/ai/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me financial reports"}'
```

---

## Option 2: Run app_enhanced.py (Gemini-based with Enhanced Features)

### Step 1: Set Gemini API Key (Optional)
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

**Note:** If you don't have a Gemini key, it will run in demo mode.

### Step 2: Navigate to Project
```bash
cd /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub
```

### Step 3: Start the Enhanced Server
```bash
python3 app_enhanced.py
```

You should see:
```
✅ Gemini Assistant Initialized (or demo mode message)
🚀 Server running on http://localhost:5000
```

### Step 4: Access the Web Dashboard
- Open your browser and go to: **http://localhost:5000**
- You'll see the full web dashboard interface
- All features are available through the web UI

---

## Option 3: Quick Demo (No API Keys Required)

### Using start_demo.py
```bash
cd /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub
python3 start_demo.py
```

This will:
- Generate data if missing
- Start the backend server
- Work with fallback responses (no API key needed)

Then open `index2.html` in your browser.

---

## Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
pip3 install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill

# Or change the port in the Python file
```

### Issue: "Data not found"
**Solution:**
```bash
python3 generate_mock_data.py
python3 web_scraper.py
```

### Issue: API Key Not Working
**Solution:**
- The app works without API keys using fallback mode
- For enhanced responses, set the API key as shown above
- Check the API key is correct

---

## Available Endpoints (Backend_api1.py)

- `GET /customers` - Get all customers
- `GET /inventory` - Get inventory
- `GET /financials` - Get financial summary
- `GET /purchases` - Get all purchases
- `GET /purchases/<customer_id>` - Get customer purchases
- `GET /invoice/<purchase_id>` - Get invoice
- `GET /competitors` - Get competitor data
- `GET /loyalty/active-customers` - Get loyalty rewards
- `GET /store-design/current` - Get store design
- `POST /ai/query` - AI-powered queries

## Enhanced Endpoints (app_enhanced.py)

- `GET /` - Web dashboard
- `GET /api/overview` - Day-wise overview
- `GET /api/financials/insights` - AI financial insights
- `GET /api/financials/tax-advice` - Tax advice
- `GET /api/inventory/automation` - Inventory automation
- `GET /api/sku/market-analysis` - Market analysis
- `POST /ai/chatbot` - Enhanced chatbot

---

## Quick Commands Reference

```bash
# Start Backend_api1.py
export OPENAI_API_KEY="your_key"
python3 Backend_api1.py

# Start app_enhanced.py
export GEMINI_API_KEY="your_key"
python3 app_enhanced.py

# Run demo
python3 start_demo.py

# Generate data
python3 generate_mock_data.py

# Test everything
python3 test_all_features.py
```

---

## What Happens When You Run

1. **Server starts** on http://localhost:5000
2. **Data loads** from `data/data.json`
3. **AI initializes** (OpenAI or Gemini, or falls back to demo mode)
4. **Endpoints become available** for API calls
5. **Frontend can connect** to the backend

---

## Next Steps After Starting

1. **Test the API:**
   ```bash
   curl http://localhost:5000/customers
   ```

2. **Open Frontend:**
   - Open `index2.html` in browser (for Backend_api1.py)
   - Or visit http://localhost:5000 (for app_enhanced.py)

3. **Try AI Assistant:**
   - Go to AI Assistant tab
   - Ask questions like:
     - "Show me financial reports"
     - "What products need restocking?"
     - "Recommend loyalty rewards"

Enjoy your AI-powered e-commerce assistant! 🚀

