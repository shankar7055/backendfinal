import os
import json
import re
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiAssistant:
    """
    Manages interactions with Google's Gemini API.
    Drop-in replacement for the previous OpenAIAssistant.
    """
    def __init__(self, model_name="gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_insight(self, system_prompt, data_context):
        """
        Generates text analysis based on data.
        Gemini doesn't use 'system' roles the same way, so we combine prompts.
        """
        combined_prompt = (
            f"ROLE: {system_prompt}\n\n"
            f"DATA CONTEXT:\n{json.dumps(data_context, indent=2)}\n\n"
            "TASK: Analyze the data and provide the requested summary."
        )
        
        try:
            response = self.model.generate_content(combined_prompt)
            return response.text
        except Exception as e:
            return f"Gemini Insight Error: {e}"

    def chatbot_query(self, user_query, business_context):
        """
        Handles conversational queries.
        """
        system_instruction = (
            "You are a friendly, expert E-commerce Business Assistant. "
            "Use the provided business data context to answer the user's query accurately. "
            "If the data doesn't contain the answer, offer general business advice."
        )
        
        combined_prompt = (
            f"{system_instruction}\n\n"
            f"CURRENT BUSINESS DATA:\n{json.dumps(business_context, indent=2)}\n\n"
            f"USER QUERY: {user_query}"
        )
        
        try:
            response = self.model.generate_content(combined_prompt)
            raw_text = response.text if hasattr(response, 'text') else str(response)
            return self._format_response(raw_text)
        except Exception as e:
            logging.exception("Gemini chatbot query failed")
            return "Sorry, I'm having trouble answering right now. Please try again."    

    def _format_response(self, text: str) -> str:
        """Normalize and pretty-print the model response for end users.

        - Strips surrounding quotes and whitespace.
        - If the model returned JSON, pretty-print it.
        - Collapse excessive blank lines and ensure the text ends with punctuation.
        """
        if not text:
            return ""

        text = text.strip()

        # Remove wrapping quotes if present
        if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
            text = text[1:-1].strip()

        # Try to parse JSON and pretty-print for readability
        try:
            parsed = json.loads(text)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except Exception:
            pass

        # Collapse more than two newlines into two
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Trim repeated whitespace
        text = re.sub(r"[ \t]{2,}", " ", text)

        # Ensure punctuation at the end for better readability in UI
        if not re.search(r"[.!?]\s*$", text):
            text = text.rstrip() + '.'

        return text

    def generate_structured_analysis(self, prompt, schema=None):
        """
        Generates JSON output.
        Gemini 1.5 Flash supports native JSON mode.
        """
        try:
            # Configure the model to return JSON
            json_model = genai.GenerativeModel(
                self.model.model_name,
                generation_config={"response_mime_type": "application/json"}
            )
            
            combined_prompt = (
                "You are an expert market analyst. "
                f"{prompt}\n"
                "Respond strictly with valid JSON."
            )
            
            response = json_model.generate_content(combined_prompt)
            return json.loads(response.text)
        except Exception as e:
            return {"error": "Structured Analysis Error", "details": str(e)}

    def classify_query(self, query):
        """
        Classifies the user's query intent.
        """
        prompt = (
            "Classify the following user query into ONE of these categories: "
            "FINANCIALS, INVENTORY, LOYALTY, CHATBOT, COMPETITOR, GROWTH, WEBSITE_HEALTH.\n"
            f"Query: {query}\n"
            "Respond only with the category name."
        )
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().upper()
        except Exception as e:
            return f"CLASSIFICATION_ERROR: {e}"