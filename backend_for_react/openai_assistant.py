import openai
import os
import json
from typing import Dict, Any

class OpenAIAssistant:
    """
    OpenAI-based assistant to replace Google Gemini API
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_response(self, prompt: str, max_tokens: int = 150) -> str:
        """Generate response using OpenAI GPT"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful e-commerce assistant. Respond with only one keyword from: financials, restock, reward, design, website. No explanation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def classify_query(self, user_query: str) -> str:
        """Classify user query into predefined categories"""
        prompt = f"""User query: {user_query}
        Respond with only one keyword from: financials, restock, reward, design, website.
        No explanation. Just the keyword."""
        
        return self.generate_response(prompt, max_tokens=10)

