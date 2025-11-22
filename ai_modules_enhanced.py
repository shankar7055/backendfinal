# ai_modules.py

import pandas as pd
import numpy as np
import random
import os
import json
from datetime import datetime
from gemini_assistant import GeminiAssistant 
import logging

logger = logging.getLogger(__name__)

class AIModules:
    def __init__(self, data, ai_assistant: GeminiAssistant):
        self.data = data
        self.products_data = {p['product_id']: p for p in data.get('products', [])}
        self.customers_data = {c['customer_id']: c for c in data.get('customers', [])}
        self.df_purchases = self._prepare_data()
        self.ai_assistant = ai_assistant # Injecting the Gemini assistant

    def _prepare_data(self):
        """Prepares the purchases data into a Pandas DataFrame for analysis."""
        purchases = self.data.get('purchases', [])
        if not purchases:
            return pd.DataFrame()
        
        df = pd.DataFrame(purchases)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.normalize()
        df['revenue'] = df['quantity'] * df['price']
        
        # Merge cost data
        product_costs = {p['product_id']: p.get('cost', 0) for p in self.data.get('products', [])}
        df['cost_of_goods'] = df.apply(lambda row: row['quantity'] * product_costs.get(row['product_id'], 0), axis=1)
        df['profit'] = df['revenue'] - df['cost_of_goods']
        return df

    # --- Data Serving Methods (Unchanged) ---
    def get_customers(self):
        return self.data.get('customers', [])

    def get_inventory(self):
        return self.data.get('products', [])

    def get_competitor_data(self):
        try:
            with open('data/competitor_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": "Competitor data not found. Please run the web_scraper.py script first."}
    
    # --- CORE BUSINESS LOGIC (Refactored for GenAI) ---

    def get_financial_summary(self):
        """Calculates raw financial metrics (P&L)."""
        if self.df_purchases.empty:
            return {"error": "No purchase data available."}

        # 1. Sales & Profit
        total_revenue = self.df_purchases['revenue'].sum()
        total_cogs = self.df_purchases['cost_of_goods'].sum()
        gross_profit = total_revenue - total_cogs
        
        # 2. Expenses
        operating_expenses = sum(e.get('amount', 0) for e in self.data.get('expenses', []))

        # 3. Final Profit & Tax
        net_profit = gross_profit - operating_expenses
        tax_rate = 0.15 # Mock Tax Rate
        tax_payable = net_profit * tax_rate if net_profit > 0 else 0
        
        return {
            "TotalRevenue": round(total_revenue, 2),
            "TotalCOGS": round(total_cogs, 2),
            "GrossProfit": round(gross_profit, 2),
            "OperatingExpenses": round(operating_expenses, 2),
            "NetProfit": round(net_profit, 2),
            "TotalSalesCount": len(self.df_purchases),
            "TaxRate_Mock": tax_rate,
            "EstimatedTaxPayable": round(tax_payable, 2)
        }

    def get_financial_insights(self):
        """
        GenAI-Powered Financial Management & CA Work Summary.
        Takes raw data and generates a professional P&L analysis.
        """
        raw_financials = self.get_financial_summary()
        
        system_prompt = (
            "You are a Chartered Accountant (CA) for an e-commerce business. "
            "Analyze the provided financial summary (P&L) and write a concise, one-paragraph executive summary. "
            "Include key figures like Net Profit and Gross Profit, and give one piece of tax-related advice."
        )
        
        ca_summary = self.ai_assistant.generate_insight(system_prompt, raw_financials)
        
        return {
            "raw_financial_data": raw_financials,
            "ca_summary_report": ca_summary
        }
        
    def get_tax_deduction_advice(self):
        """
        GenAI-Powered Tax Deduction Help.
        """
        expenses = self.data.get('expenses', [])
        
        system_prompt = (
            "You are a tax expert helping a business owner with ITR filing. "
            "Review the list of operating expenses and highlight which expenses are typically 100% deductible for an e-commerce business. "
            "Provide three clear, specific tips for maximizing deductions during ITR filing. Format the advice in bullet points."
        )
        
        # Pass expense data and financial context to the model
        data_context = {
            "OperatingExpensesList": [e['description'] for e in expenses],
            "TotalOperatingExpenses": sum(e.get('amount', 0) for e in expenses)
        }

        tax_advice = self.ai_assistant.generate_insight(system_prompt, data_context)
        
        return {
            "expense_list": expenses,
            "tax_deduction_advice": tax_advice
        }

    def analyze_inventory_and_restock(self):
        """
        Combines local inventory analysis with GenAI for actionable procurement suggestions.
        """
        # 1. Local Data Analysis: Find low stock items using dynamic safety thresholds
        low_stock_data = []
        # Calculate sales velocity per product over last 30 days
        recent_window_days = 30
        cutoff_date = None
        if not self.df_purchases.empty:
            cutoff_date = self.df_purchases['date'].max() - pd.Timedelta(days=recent_window_days)

        for product_id, product_info in self.products_data.items():
            current_stock = product_info.get('stock_level', 0)

            # Compute average daily sales for this product in the recent window
            if not self.df_purchases.empty:
                recent_sales = self.df_purchases[
                    (self.df_purchases['product_id'] == product_id) &
                    (self.df_purchases['date'] > cutoff_date)
                ]
                total_qty = int(recent_sales['quantity'].sum()) if not recent_sales.empty else 0
                avg_daily_sales = total_qty / recent_window_days
            else:
                total_qty = 0
                avg_daily_sales = 0

            # Dynamic safety threshold based on lead time and sales velocity
            lead_time_days = 14  # Mock supplier lead time
            safety_factor = 1.5
            dynamic_threshold = max(50, int((avg_daily_sales * lead_time_days) * safety_factor))

            # Compute recommended order quantity to reach target stock covering lead time + 7 days buffer
            target_stock = int((avg_daily_sales * (lead_time_days + 7)) * safety_factor)
            recommendation_qty = max(0, target_stock - current_stock)

            if current_stock <= dynamic_threshold:
                low_stock_data.append({
                    "product_id": product_id,
                    "name": product_info.get('name', 'Unknown Product'),
                    "current_stock": current_stock,
                    "sales_in_last_30_days": total_qty,
                    "avg_daily_sales": round(avg_daily_sales, 3),
                    "dynamic_threshold": dynamic_threshold,
                    "recommendation_qty": recommendation_qty
                })
        
        if not low_stock_data:
            return {"status": "OK", "inventory_summary": "All stock levels are healthy."}

        # 2. GenAI Analysis: Generate actionable email trigger
        system_prompt = (
            "You are an Inventory Manager. Based on the low stock report, draft a concise, formal email "
            "to the owner/procurement team detailing the items that need immediate restocking. "
            "Include the name, current stock, and recommended order quantity for each item."
        )
        
        email_draft = self.ai_assistant.generate_insight(system_prompt, {"LowStockReport": low_stock_data})
        
        return {
            "low_stock_report": low_stock_data,
            "restock_email_draft": email_draft,
            "trigger_action": "Email sent to procurement."
        }
        
    def analyze_ecom_growth_and_trends(self):
        """
        Performs time-series analysis and uses GenAI for interpretation.
        """
        if self.df_purchases.empty:
            return {"error": "No data for growth analysis."}

        # 1. Local Data Analysis: Aggregate daily sales
        daily_sales = self.df_purchases.groupby('date')['revenue'].sum().reset_index()
        
        # 2. Simple Trend/Anomaly Detection (Prototype level)
        # Calculate recent vs historical performance
        total_days = (daily_sales['date'].max() - daily_sales['date'].min()).days
        if total_days < 1:
            return {"error": "Need more data for trend analysis."}
            
        recent_days = 7
        recent_revenue = daily_sales['revenue'].tail(recent_days).sum()
        average_daily_revenue = daily_sales['revenue'].mean()
        
        growth_data = {
            "TotalRevenue": daily_sales['revenue'].sum(),
            "TotalDaysTracked": total_days,
            "AverageDailyRevenue": round(average_daily_revenue, 2),
            "Last7DayRevenue": round(recent_revenue, 2),
            "Last7DayAvg": round(recent_revenue / recent_days, 2),
            "Performance_vs_Average": f"{round(((recent_revenue / recent_days) / average_daily_revenue - 1) * 100, 2)}%"
        }

        # 3. GenAI Interpretation
        system_prompt = (
            "You are a strategic E-commerce Growth Analyst. "
            "Analyze the provided growth metrics. Identify the key performance indicator (KPI) change. "
            "Suggest one marketing or product strategy based on the recent trend (positive or negative)."
        )

        growth_summary = self.ai_assistant.generate_insight(system_prompt, growth_data)

        # Local anomaly detection: compare last 7-day average with historical average
        last7_avg = recent_revenue / recent_days
        historical_avg = average_daily_revenue
        pct_change = ((last7_avg - historical_avg) / historical_avg) * 100 if historical_avg else 0
        anomaly = None
        if pct_change >= 20:
            anomaly = "positive_spike"
        elif pct_change <= -20:
            anomaly = "negative_drop"

        local_insights = {
            "Last7DayAvg": round(last7_avg, 2),
            "HistoricalAvg": round(historical_avg, 2),
            "PercentChange": round(pct_change, 2),
            "AnomalyType": anomaly
        }

        return {
            "daily_sales_data": daily_sales.to_dict('records'),
            "growth_metrics": growth_data,
            "growth_strategy_advice": growth_summary,
            "local_insights": local_insights
        }

    def analyze_sku_market_and_trend(self, competitor_data, product_id='P001'):
        """
        Performs market analysis for a specific SKU using scraped and internal data,
        then uses GenAI to interpret the findings.
        """
        internal_product = self.products_data.get(product_id)
        if not internal_product:
            return {"error": f"Product ID {product_id} not found."}

        # 1. Local Data Analysis: Price gap
        internal_price = internal_product['price']
        
        # Find competitor closest in price/name (simple mock matching)
        closest_competitor = min(
            competitor_data, 
            key=lambda x: abs(x['price'] - internal_price)
        )

        market_data = {
            "InternalProduct": internal_product,
            "ClosestCompetitor": closest_competitor,
            "PriceGap": round(internal_price - closest_competitor['price'], 2)
        }

        # 2. GenAI Interpretation: Dynamic pricing recommendation
        system_prompt = (
            f"You are a Dynamic Pricing Strategist. Analyze the internal price of Product {product_id} "
            f"against its closest competitor ({closest_competitor['product_name']}). "
            "Provide a specific pricing recommendation (e.g., 'Increase price to X' or 'Offer a 10% discount') "
            "and justify it in one sentence."
        )

        pricing_advice = self.ai_assistant.generate_insight(system_prompt, market_data)

        # Compute a conservative pricing recommendation locally to accompany GenAI advice
        internal_cost = internal_product.get('cost', 0)
        internal_price = internal_product.get('price', internal_price)
        competitor_price = closest_competitor.get('price', internal_price)

        # Maintain minimum margin
        min_margin = 0.20
        min_price_to_maintain_margin = internal_cost / (1 - min_margin) if (1 - min_margin) > 0 else internal_price

        if competitor_price < internal_price:
            # Try to undercut slightly but not violate min margin
            recommended_price = max(competitor_price - 0.01, min_price_to_maintain_margin)
            action = f"Consider reducing price to {round(recommended_price,2)} to be competitive with {closest_competitor['product_name']}."
        else:
            # Competitor is priced higher; recommend maintaining or increasing price slightly
            recommended_price = max(internal_price, min_price_to_maintain_margin)
            action = f"Competitor prices are higher; you may maintain price at {round(recommended_price,2)} or test a small premium."

        market_data.update({
            "ComputedRecommendation": {
                "recommended_price": round(recommended_price, 2),
                "reason": action
            }
        })

        return {
            "product_market_data": market_data,
            "pricing_recommendation": pricing_advice,
            "computed_recommendation": market_data["ComputedRecommendation"]
        }

    def get_active_customer_loyalty_rewards(self):
        """
        Returns top customers by total spend. Compatible with demo response format.
        """
        # Compute total spent per customer from purchases
        if self.df_purchases.empty:
            return {"top_customers": []}

        totals = self.df_purchases.groupby('customer_id').apply(lambda df: (df['quantity'] * df['price']).sum())
        totals = totals.sort_values(ascending=False)
        top = []
        for cid, amt in totals.head(10).items():
            customer = self.customers_data.get(cid, {"name": cid})
            top.append({
                "name": customer.get('name', cid),
                "total_spent": round(float(amt), 2)
            })

        return {"top_customers": top}

    def get_inventory_trends(self, product_id='P001', days=30):
        """
        Returns a timeseries of daily sold quantity for the given product over the past `days` days.
        """
        if self.df_purchases.empty:
            return {"error": "No purchase data available.", "series": []}

        end = self.df_purchases['date'].max()
        start = end - pd.Timedelta(days=days)

        df = self.df_purchases[
            (self.df_purchases['product_id'] == product_id) &
            (self.df_purchases['date'] > start)
        ]

        # Group by date and sum quantity
        grouped = df.groupby('date')['quantity'].sum().reset_index()

        # Build full series with days having zero sales
        series = []
        for i in range(days):
            d = (start + pd.Timedelta(days=i+1)).normalize()
            match = grouped[grouped['date'] == d]
            qty = int(match['quantity'].iloc[0]) if not match.empty else 0
            series.append({"date": d.isoformat(), "quantity": qty})

        return {"product_id": product_id, "series": series}

    # --- Other Methods (Simplified or moved to GenAI) ---
    def generate_store_design_idea(self, trend="Modern", store_type="fashion boutique"):
        """
        MOCK: GenAI is used here to generate the text description of a new design idea.
        """
        system_prompt = (
            f"Generate a creative, detailed store design concept (layout, colors, typography) "
            f"for an e-commerce website selling '{store_type}' using a '{trend}' style. "
            "Provide the output as a detailed text description."
        )
        
        design_description = self.ai_assistant.generate_insight(system_prompt, {"CurrentDesignNotes": self.get_current_store_design_preview()})

        # Return structured mock data + the GenAI description
        return {
            "trend": trend,
            "design_description": design_description,
            "mock_preview_url": f"https://via.placeholder.com/800x450/4A90E2/FFFFFF?text={trend.replace(' ', '+')}+GenAI+Design"
        }
    
    def get_invoice(self, purchase_id):
        """Generates mock invoice data based on purchase ID."""
        sale = next((s for s in self.data.get('purchases', []) if s.get('purchase_id') == purchase_id), None)
        # ... [rest of the get_invoice logic remains the same]
        if not sale:
            return {"error": "Purchase ID not found"}

        product = self.products_data.get(sale.get('product_id'))
        customer = self.customers_data.get(sale.get('customer_id'))

        if not product or not customer:
            return {"error": "Product or customer data for this sale is missing."}

        quantity = sale.get('quantity', 0)
        price = sale.get('price', 0)
        total_price = quantity * price if quantity and price else 0
        
        invoice_data = {
            "invoice_id": f"INV-{purchase_id}",
            "date": sale.get('timestamp'),
            "customer": {
                "name": customer.get('name'),
                "customer_id": customer.get('customer_id')
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
            "invoice_total": total_price,
            "note": "This invoice was automatically generated by the AI Hub.",
        }
        return invoice_data