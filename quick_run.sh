#!/bin/bash

echo "=========================================="
echo "E-Commerce AI Assistant - Quick Run"
echo "=========================================="
echo ""

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo "   The app will work with fallback responses"
    echo ""
    read -p "Do you want to set it now? (y/n): " set_key
    if [ "$set_key" = "y" ]; then
        export OPENAI_API_KEY="REDACTED_OPENAI_KEY3WfRbAALDeR816OT3BlbkFJA40H3MjYg9wkMCfxK2hIBTbZdY0wcU2UUk4Rf8KiZebnaEKlz2SVlcyNTqhRdU3L_eIbja6p0A"
        echo "✅ API key set"
    fi
else
    echo "✅ OPENAI_API_KEY is set"
fi

echo ""
echo "Choose which backend to run:"
echo "1. Backend_api1.py (OpenAI-based) - Recommended"
echo "2. app_enhanced.py (Gemini-based with enhanced features)"
echo "3. start_demo.py (Demo mode, no API keys)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Backend_api1.py..."
        echo "Server will run on http://localhost:5000"
        echo "Open index2.html in your browser"
        echo ""
        python3 Backend_api1.py
        ;;
    2)
        echo ""
        echo "Starting app_enhanced.py..."
        echo "Server will run on http://localhost:5000"
        echo "Open http://localhost:5000 in your browser"
        echo ""
        python3 app_enhanced.py
        ;;
    3)
        echo ""
        echo "Starting demo mode..."
        python3 start_demo.py
        ;;
    *)
        echo "Invalid choice. Starting Backend_api1.py by default..."
        python3 Backend_api1.py
        ;;
esac
