"""
Demo mode fallback when Gemini is not available.
Provides mock responses for testing the frontend.
"""

class DemoAIModules:
    """Mock AI modules for demo purposes when Gemini is unavailable."""
    
    def __init__(self):
        self.demo_data = {
            "total_revenue": 125000,
            "net_profit": 25000,
            "total_expenses": 100000,
            "growth_rate": 15.5,
            "total_orders": 450
        }
    
    def get_financial_insights(self):
        return {
            "financial_summary": {
                "total_revenue": self.demo_data["total_revenue"],
                "net_profit": self.demo_data["net_profit"],
                "total_expenses": self.demo_data["total_expenses"]
            },
            "ai_insights": "Demo Mode: Revenue is trending upward. Consider expanding marketing budget."
        }
    
    def analyze_inventory_and_restock(self):
        return {
            "low_stock_report": [
                {"product_name": "Demo Product A", "current_stock": 15},
                {"product_name": "Demo Product B", "current_stock": 8}
            ],
            "restock_email_draft": "Demo Mode: Please restock low inventory items."
        }
    
    def get_active_customer_loyalty_rewards(self):
        return {
            "top_customers": [
                {"name": "Demo Customer 1", "total_spent": 5000},
                {"name": "Demo Customer 2", "total_spent": 3500},
                {"name": "Demo Customer 3", "total_spent": 2800}
            ]
        }
    
    def analyze_ecom_growth_and_trends(self):
        return {
            "growth_metrics": self.demo_data,
            "daily_sales_data": []
        }

def get_demo_chatbot_response(query):
    """Returns demo responses for common queries."""
    responses = {
        "revenue": "Demo Mode: Your current revenue is ₹125,000 with a growth rate of 15.5%.",
        "inventory": "Demo Mode: You have 2 products with low stock that need restocking.",
        "customers": "Demo Mode: Your top customer has spent ₹5,000 this month.",
        "default": "Demo Mode: I'm running in demo mode. Please configure your GEMINI_API_KEY for full functionality."
    }
    
    query_lower = query.lower()
    for key, response in responses.items():
        if key in query_lower:
            return response
    
    return responses["default"]