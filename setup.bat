@echo off
REM Setup script for Confucius Chatbot (Windows)

echo 📜 Setting up Confucius Chatbot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7 or higher.
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install packages
echo 📦 Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Failed to install packages. Please check the error messages above.
    exit /b 1
) else (
    echo.
    echo ✅ All packages installed successfully!
    echo.
    echo 🚀 To run the app:
    echo    1. Activate the virtual environment: venv\Scripts\activate
    echo    2. Run: streamlit run app.py
    echo.
    echo 💡 Or use the run script: run.bat
    echo.
)

