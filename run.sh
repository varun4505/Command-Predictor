#!/bin/bash
# AI Terminal Command Analyzer - Linux/macOS Runner

echo "AI Terminal Command Analyzer"
echo "==========================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please make sure the .env file exists with your Groq API key"
    echo "You can copy from .env.example and add your API key"
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import groq, dotenv, requests, psutil" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Run the analyzer
echo "Starting AI agent..."
python3 main.py "$@"

if [ $? -ne 0 ]; then
    echo
    echo "Error occurred. Check the output above for details."
    read -p "Press Enter to continue..."
fi
