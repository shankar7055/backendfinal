from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

from ai_modules import AIModules
from openai_assistant import OpenAIAssistant
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI assistant
try:
    openai_assistant = OpenAIAssistant()
except ValueError as e:
    logger.warning(f"OpenAI not available: {e}")
    openai_assistant = None

# --- Load your e-commerce data from JSON ---
def load_data():
    try:
        with open('data/data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("data/data.json not found.")
        return {}

# Cache data and AI modules
cached_data = load_data()
cached_ai_modules = AIModules(cached_data) if cached_data else None

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>Gemini Pro AI API is Running ✅</h1><p>Try POST /ai/query</p>"

@app.route('/customers', methods=['GET'])
def get_customers_route():
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_customers())

@app.route('/inventory', methods=['GET'])
def get_inventory_route():
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_inventory())

# Route for all purchases
@app.route('/purchases', methods=['GET'])
def get_all_purchases_route():
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_all_purchases())

# Route for purchases by customer_id
@app.route('/purchases/<string:customer_id>', methods=['GET'])
def get_purchases_by_customer_route(customer_id):
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_purchases(customer_id))

@app.route('/invoice/<string:purchase_id>', methods=['GET'])
def get_invoice_route(purchase_id):
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_invoice(purchase_id))

@app.route('/financials', methods=['GET'])
def get_financials_route():
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_financials())

@app.route('/competitors', methods=['GET'])
def get_competitors_route():
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_competitor_data())

# Route to get loyalty rewards for active customers
@app.route('/loyalty/active-customers', methods=['GET'])
def get_active_customer_loyalty_rewards_route():
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_active_customer_loyalty_rewards())

# NEW ROUTE: Get current store design preview
@app.route('/store-design/current', methods=['GET'])
def get_current_store_design_preview_route():
    if not cached_ai_modules:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(cached_ai_modules.get_current_store_design_preview())


# --- AI Query Route ---
@app.route('/ai/query', methods=['POST'])
def ai_query():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"error": "No query provided."}), 400

    if not cached_ai_modules:
        return jsonify({"response": "Data not available. Please check system configuration."}), 500

    try:
        # Use OpenAI to classify the query or fallback to keyword matching
        if openai_assistant:
            tool = openai_assistant.classify_query(user_query).lower()
        else:
            tool = classify_query_fallback(user_query)

        # Route to appropriate AI module based on classification
        if "financial" in tool:
            output = cached_ai_modules.get_financials()
        elif "restock" in tool or "inventory" in tool:
            output = cached_ai_modules.analyze_inventory_and_restock()
        elif "reward" in tool or "loyalty" in tool:
            # Extract customer ID if mentioned, otherwise use default
            customer_id = extract_customer_id(user_query) or "C001"
            output = cached_ai_modules.recommend_loyalty_rewards(customer_id)
        elif "design" in tool:
            # Extract trend if mentioned, otherwise use default
            trend = extract_trend(user_query) or "Minimalist"
            output = cached_ai_modules.generate_store_design_idea(trend)
        elif "website" in tool or "bug" in tool or "problem" in tool:
            output = cached_ai_modules.detect_website_problems()
        elif "competitor" in tool or "price" in tool:
            output = cached_ai_modules.get_competitor_data()
        elif "customer" in tool:
            output = cached_ai_modules.get_customers()
        elif "product" in tool:
            output = cached_ai_modules.get_inventory()
        else:
            output = "I can help you with: financials, inventory/restocking, loyalty rewards, store design, website health, competitor analysis, customer data, and product information. What would you like to know?"

        return jsonify({"response": output})
    except Exception as e:
        logger.error(f"AI Query Error: {str(e)}")
        return jsonify({"response": f"Error processing request: {str(e)}"}), 500

def classify_query_fallback(query):
    """Fallback query classification when OpenAI is not available"""
    query_lower = query.lower()
    if any(word in query_lower for word in ['money', 'profit', 'revenue', 'financial', 'sales']):
        return 'financials'
    elif any(word in query_lower for word in ['stock', 'inventory', 'restock', 'supply']):
        return 'restock'
    elif any(word in query_lower for word in ['reward', 'loyalty', 'customer']):
        return 'reward'
    elif any(word in query_lower for word in ['design', 'theme', 'layout', 'style']):
        return 'design'
    elif any(word in query_lower for word in ['website', 'bug', 'error', 'problem']):
        return 'website'
    elif any(word in query_lower for word in ['competitor', 'competition', 'price']):
        return 'competitor'
    elif any(word in query_lower for word in ['product', 'item']):
        return 'product'
    return 'unknown'

def extract_customer_id(query):
    """Extract customer ID from query if mentioned"""
    import re
    match = re.search(r'C\d{3}', query.upper())
    return match.group(0) if match else None

def extract_trend(query):
    """Extract design trend from query if mentioned"""
    trends = ['modern', 'bohemian', 'industrial', 'vintage', 'minimalist']
    query_lower = query.lower()
    for trend in trends:
        if trend in query_lower:
            return trend.capitalize()
    return None

# --- Run the app ---
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5002))  # Use 5002 to avoid macOS AirTunes conflict
    app.run(debug=debug_mode, port=port, host='127.0.0.1')