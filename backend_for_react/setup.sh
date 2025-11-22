#!/bin/bash

echo "🚀 Setting up Backend for React Frontend..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python3 -m venv venv 2>/dev/null || echo "Virtual environment already exists or venv not available"

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Generate mock data
echo "📊 Generating mock data..."
python3 generate_mock_data.py

# Generate competitor data
echo "🔍 Generating competitor data..."
python3 web_scraper.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the backend server:"
echo "  python3 app.py"
echo ""
echo "The server will run on http://127.0.0.1:5000"
echo ""
echo "Optional: Set OPENAI_API_KEY environment variable for AI features"
echo "  export OPENAI_API_KEY='your_key_here'"

