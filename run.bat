@echo off
echo.
echo ========================================
echo    Student Feedback System
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing/Checking dependencies...
py -m pip install -r requirements.txt

REM Run the application
echo.
echo Starting Streamlit application...
echo The application will open in your default browser
echo Press Ctrl+C to stop the server
echo.
py -m streamlit run main.py

pause
