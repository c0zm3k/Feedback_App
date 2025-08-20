#!/bin/bash

echo ""
echo "========================================"
echo "    Student Feedback System"
echo "========================================"
echo ""
echo "Starting the application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Install requirements if needed
echo "Installing/Checking dependencies..."
pip3 install -r requirements.txt

# Run the application
echo ""
echo "Starting Streamlit application..."
echo "The application will open in your default browser"
echo "Press Ctrl+C to stop the server"
echo ""
streamlit run main.py
