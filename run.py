#!/usr/bin/env python3
"""
Student Feedback System - Launcher Script
This script provides an easy way to run the feedback system.
"""

import subprocess
import sys
import os

def main():
    """Main function to run the Streamlit application"""
    print("🚀 Starting Student Feedback System...")
    print("📝 Loading application...")
    
    try:
        # Check if streamlit is installed
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
    
    # Run the application
    print("🌐 Starting web server...")
    print("📱 The application will be available at: http://localhost:8501")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py", "--server.headless", "true"])

if __name__ == "__main__":
    main()
