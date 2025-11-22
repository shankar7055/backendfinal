# ai_modules.py

import pandas as pd
import random
import os
import json 

class AIModules:
    def __init__(self, data):
        self.data = data
        self.products_data = {p['product_id']: p for p in data.get('products', [])}
        self.customers_data = {c['customer_id']: c for c in data.get('customers', [])}

    # --- Data Serving Methods ---
    def get_customers(self):
        """Returns a list of all customer objects."""
        return self.data.get('customers', [])

    def get_purchases(self, customer_id):
        """Returns the purchase history for a specific customer."""
        purchases = [p for p in self.data.get('purchases', []) if p.get('customer_id') == customer_id]
        return purchases

    def get_all_purchases(self):
        """Returns a list of all purchase objects."""
        return self.data.get('purchases', [])

    def get_inventory(self):
        """Returns a list of all products with their current stock levels."""
        return self.data.get('products', [])

    def get_competitor_data(self):
        """Reads competitor data from a JSON file."""
        try:
            with open('data/competitor_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": "Competitor data not found. Please run the web_scraper.py script first."}

    # Method to get details of the current store design
    def get_current_store_design_preview(self):
        """
        Simulates retrieving details of the current live store design.
        In a real scenario, this would fetch from a database or CMS.
        """
        current_design = {
            "name": "Current E-commerce Theme v3.2",
            "description": "Our existing clean and functional design. Optimized for fast loading but could benefit from a modern refresh. It features a simple header, a main content area with product grids, and a basic footer. Colors are muted with primary green accents.",
            "last_updated": "2024-03-10",
            "style_elements": {
                "layout_summary": "Standard 2-column layout for product listings, single-column product detail page.",
                "color_palette": ["#F8F8F8", "#4A4A4A", "#A0A0A0", "#008000"],
                "typography": {"headings": "Arial, sans-serif", "body": "Helvetica, sans-serif"},
                "interactive_elements": "Simple button hovers, no complex animations."
            },
            "mock_preview_url": "https://via.placeholder.com/800x450/e0e0e0/555555?text=Existing+Store+Design+Preview" # Mock image
        }
        return {"current_store_design": current_design}

    # --- AI Module Methods ---
    def recommend_loyalty_rewards(self, customer_id):
        """
        AI for Loyalty Rewards: Suggests personalized rewards.
        (Simplified example for hackathon: recommends a product not recently purchased by the customer)
        """
        customer_purchases_ids = [p['product_id'] for p in self.data.get('purchases', []) if p.get('customer_id') == customer_id]
        
        available_products_ids = list(self.products_data.keys())
        
        unpurchased_products_ids = [prod_id for prod_id in available_products_ids if prod_id not in customer_purchases_ids]
        
        if not unpurchased_products_ids:
            return {"customer_id": customer_id, "recommendation": "Customer has purchased all available products! Consider offering a generic discount or a new product preview."}
        
        recommended_product_id = random.choice(unpurchased_products_ids)
        recommended_product_name = self.products_data.get(recommended_product_id, {}).get('name', 'an exciting new item')
        
        return {
            "customer_id": customer_id,
            "recommendation": f"As a thank you for being a valued customer, we recommend a special loyalty reward: 15% off your next purchase of {recommended_product_name}!"
        }

    def get_active_customer_loyalty_rewards(self):
        """
        AI for Loyalty Rewards: Provides personalized rewards for all active customers.
        Optimized to avoid repeated data processing
        """
        # Build customer purchase cache
        customer_purchases = {}
        for purchase in self.data.get('purchases', []):
            customer_id = purchase.get('customer_id')
            if customer_id:
                if customer_id not in customer_purchases:
                    customer_purchases[customer_id] = []
                customer_purchases[customer_id].append(purchase)
        
        recommendations = []
        if not customer_purchases:
            return {"message": "No active customers found to generate loyalty rewards for."}

        for customer_id, purchases in customer_purchases.items():
            customer_name = self.customers_data.get(customer_id, {}).get('name', 'Unknown Customer')
            rec_data = self.recommend_loyalty_rewards(customer_id)
            recommendations.append({
                "customer_id": customer_id,
                "customer_name": customer_name,
                "reward": rec_data.get("recommendation", "No specific recommendation.")
            })
        
        return {"active_customer_loyalty_rewards": recommendations}


    def analyze_inventory_and_restock(self):
        """
        AI for Inventory Management: Provides low stock alerts and restocking recommendations.
        Dynamic thresholds based on product data
        """
        low_stock_alerts = []
        restocking_recommendations = []

        for product_id, product_info in self.products_data.items():
            current_stock = product_info.get('stock_level', 0)
            # Dynamic threshold based on product characteristics
            threshold = max(50, current_stock * 0.2)  # At least 50 or 20% of current stock
            
            if current_stock < threshold:
                low_stock_alerts.append({
                    "product_id": product_id,
                    "name": product_info.get('name', 'Unknown Product'),
                    "current_stock": current_stock,
                    "threshold": threshold,
                    "alert": "Low Stock",
                    "recommendation": "Restock immediately! Current stock is below critical level."
                })
                # Dynamic order quantity
                order_qty = max(100, threshold * 2)
                restocking_recommendations.append({
                    "product_id": product_id,
                    "name": product_info.get('name', 'Unknown Product'),
                    "order_quantity": order_qty
                })
        
        return {
            "low_stock_alerts": low_stock_alerts,
            "restocking_recommendations": restocking_recommendations
        }

    def analyze_dynamic_pricing_and_production(self):
        """
        AI for Dynamic Pricing & Production: Suggests price adjustments and production boosts.
        (Simplified: uses predefined rules for specific products)
        """
        advice = []
        
        if self.products_data.get('P001', {}).get('stock_level', 0) > 100: 
             advice.append({
                 "product_id": "P001",
                 "name": "Product 1",
                 "advice_type": "Pricing Adjustment",
                 "suggestion": "Consider a 5% price increase for Product 1 due to high assumed demand and healthy stock levels."
             })
        
        if self.products_data.get('P002', {}).get('stock_level', 0) < 80: 
            advice.append({
                "product_id": "P002",
                "name": "Product 2",
                "advice_type": "Production Boost",
                "suggestion": "Increase production of Product 2 by 20% to meet anticipated demand."
            })

        return {"dynamic_advice": advice}

    def detect_website_problems(self):
        """
        AI for Bug/Problem Warning Detection.
        Optimized string operations
        """
        mock_website_logs = [
            {"timestamp": "2025-07-18T10:00:00", "level": "ERROR", "message": "Payment gateway timeout on checkout page."},
            {"timestamp": "2025-07-18T10:05:00", "level": "INFO", "message": "User login successful for C005."},
            {"timestamp": "2025-07-18T10:10:00", "level": "WARNING", "message": "High page load time detected on product page P003."},
            {"timestamp": "2025-07-18T11:00:00", "level": "ERROR", "message": "Database connection error."}
        ]
        
        detected_problems = []
        for log_entry in mock_website_logs:
            if log_entry['level'] in ['ERROR', 'WARNING']:
                message_lower = log_entry['message'].lower()  # Cache lowercased message
                problem = {
                    "timestamp": log_entry['timestamp'],
                    "type": log_entry['level'],
                    "description": log_entry['message']
                }
                if "payment gateway" in message_lower or "checkout" in message_lower:
                    problem["suggested_fix"] = "Action: Review payment gateway logs and configuration immediately."
                elif "page load time" in message_lower:
                    problem["suggested_fix"] = "Action: Optimize image sizes and review CDN/hosting settings."
                elif "database connection error" in message_lower:
                    problem["suggested_fix"] = "Action: Check database server status and connection parameters."
                else:
                    problem["suggested_fix"] = "Action: Investigate related system logs for more details."
                detected_problems.append(problem)
        
        return {"website_problems": detected_problems}

    def generate_store_design_idea(self, trend="Modern", store_type="fashion boutique"):
        """
        AI for Store Design Ideas: Generates creative design suggestions with mock preview.
        """
        # Define some example palettes/fonts based on trends
        palettes = {
            "modern": ["#2C3E50", "#ECF0F1", "#1ABC9C", "#3498DB"],
            "bohemian": ["#A0522D", "#F5DEB3", "#8B4513", "#D2B48C"],
            "industrial": ["#34495E", "#7F8C8D", "#95A5A6", "#2C3E50"],
            "vintage": ["#8B4513", "#D2B48C", "#F0E68C", "#B0C4DE"],
            "minimalist": ["#FFFFFF", "#333333", "#E0E0E0", "#607D8B"]
        }
        typographies = {
            "modern": {"headings": "Poppins", "body": "Lato"},
            "bohemian": {"headings": "Playfair Display", "body": "Lora"},
            "industrial": {"headings": "Roboto Condensed", "body": "Open Sans"},
            "vintage": {"headings": "Lobster Two", "body": "Merriweather"},
            "minimalist": {"headings": "Montserrat", "body": "Open Sans Light"}
        }

        chosen_palette = palettes.get(trend.lower(), palettes["modern"])
        chosen_typography = typographies.get(trend.lower(), typographies["modern"])

        description_template = (
            f"For a '{store_type}' with a '{trend}' design, envision a {trend.lower()} aesthetic. "
            "Focus on clean lines, a sophisticated color palette, and clear visual hierarchy. "
            "Emphasize high-quality, styled photography of products. "
            "Implement intuitive navigation and clear calls-to-action."
        )
        
        # Add more specific details based on trend for the description
        if trend.lower() == "modern":
            description_template += " Expect crisp layouts, subtle hover effects, and a focus on user experience."
        elif trend.lower() == "bohemian":
            description_template += " Incorporate natural textures, earthy tones, and a relaxed, artistic feel. Think flowing lines and curated imperfections."
        elif trend.lower() == "industrial":
            description_template += " Utilize raw materials like concrete and metal textures, exposed elements, and strong, utilitarian typography."
        elif trend.lower() == "vintage":
            description_template += " Draw inspiration from retro eras with classic fonts, muted color schemes, and nostalgic design elements."
        elif trend.lower() == "minimalist":
            description_template += " Prioritize simplicity and functionality with ample white space, a limited color palette, and clean typography."

        design_idea = {
            "trend": trend,
            "store_type": store_type,
            "description": description_template,
            "color_palette_suggestion": chosen_palette,
            "typography_suggestion": chosen_typography,
            "layout_suggestion": f"Clean {trend.lower()} grid layout for products, sticky navigation bar, prominent full-width hero section.",
            "interactive_elements_suggestion": f"Smooth {trend.lower()} transitions on hover, subtle parallax scrolling on banners, elegant modal pop-ups.",
            "unique_element_idea": "Dynamic product showcases with smooth transitions on scroll and interactive 3D views.",
            "mock_design_preview_url": f"https://via.placeholder.com/800x450/{chosen_palette[1].replace('#', '')}/{chosen_palette[0].replace('#', '')}?text={trend.replace(' ', '+')}+Design+Mockup" # Dynamic mock image based on palette
        }
        return {"design_idea": design_idea}

    def get_financials(self):
        """
        Provides a comprehensive financial summary based on all data.
        """
        total_revenue = 0
        total_cogs = 0
        total_sales = len(self.data.get('purchases', []))

        product_costs = {p['product_id']: p.get('cost', 0) for p in self.data.get('products', [])} 

        for purchase in self.data.get('purchases', []):
            quantity = purchase.get('quantity', 0)
            price = purchase.get('price', 0)
            
            if quantity and price:  # Ensure non-zero values
                total_revenue += quantity * price
                
                product_id = purchase.get('product_id')
                cost_of_product = product_costs.get(product_id, 0)
                total_cogs += quantity * cost_of_product

        operating_expenses = sum(e.get('amount', 0) for e in self.data.get('expenses', []))

        gross_profit = total_revenue - total_cogs
        net_profit = gross_profit - operating_expenses

        tax_rate = 0.15
        tax_payable = net_profit * tax_rate if net_profit > 0 else 0

        financial_summary = {
            "total_sales_count": total_sales,
            "total_revenue": total_revenue,
            "total_cogs": total_cogs,
            "gross_profit": gross_profit,
            "operating_expenses": operating_expenses,
            "net_profit": net_profit,
            "tax_payable": tax_payable
        }
        return financial_summary 

    def get_invoice(self, purchase_id):
        """
        Simulates the generation of an invoice by returning invoice details.
        """
        sale = next((s for s in self.data.get('purchases', []) if s.get('purchase_id') == purchase_id), None)
        if not sale:
            return {"error": "Purchase ID not found"}

        product = self.products_data.get(sale.get('product_id'))
        customer = self.customers_data.get(sale.get('customer_id'))

        if not product or not customer:
            return {"error": "Product or customer data for this sale is missing."}

        # Safe arithmetic operations
        quantity = sale.get('quantity', 0)
        price = sale.get('price', 0)
        total_price = quantity * price if quantity and price else 0
        
        invoice_data = {
            "invoice_id": f"INV-{purchase_id}",
            "date": sale.get('timestamp'),
            "customer": {
                "name": customer.get('name'),
                "customer_id": customer.get('customer_id'),
                "email": customer.get('email')
            },
            "items": [
                {
                    "product_name": product.get('name'),
                    "product_id": product.get('product_id'),
                    "quantity": quantity,
                    "unit_price": price,
                    "total_price": total_price
                }
            ],
            "invoice_total": total_price
        }
        return invoice_data

