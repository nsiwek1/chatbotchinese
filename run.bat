@echo off
REM Run script for Confucius Chatbot (Windows)

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the app
streamlit run app.py

