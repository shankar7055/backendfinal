import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_competitor_data(url=None):
    """
    Simulates scraping a competitor's website for product names and prices.
    Uses mock data for security and reliability.
    """
    # Use mock data instead of actual scraping for security
    mock_competitor_products = [
        {"product_name": "Competitor Product A", "price": 25.00},
        {"product_name": "Competitor Product B", "price": 45.00},
        {"product_name": "Competitor Product C", "price": 60.00},
        {"product_name": "Premium Widget", "price": 89.99},
        {"product_name": "Basic Gadget", "price": 15.50}
    ]
    
    return mock_competitor_products

def save_to_json(data, filename="competitor_data.json"):
    """
    Saves the scraped data to a JSON file inside the 'data' directory.
    Includes error handling for file operations.
    """
    # Validate filename to prevent path traversal
    if not filename or ".." in filename or "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename")
    
    try:
        # Create the 'data' directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        file_path = os.path.join('data', filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Scraped data successfully saved to '{file_path}'")
    except (IOError, OSError, PermissionError) as e:
        print(f"Error saving data: {e}")
        raise

# --- Main execution block ---
if __name__ == '__main__':
    try:
        # Run the scraper and get the data
        scraped_data = scrape_competitor_data()
        
        # Save the data to a JSON file, which your api.py will read
        save_to_json(scraped_data)
    except Exception as e:
        print(f"Error in scraper execution: {e}")

