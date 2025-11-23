#!/bin/bash

# Setup script for Confucius Chatbot

echo "📜 Setting up Confucius Chatbot..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Check for cmake (needed for pyarrow on some systems)
if ! command -v cmake &> /dev/null; then
    echo "⚠️  cmake not found. pyarrow may need it to build."
    echo "   Install with: brew install cmake"
    echo "   Or continue and pip will try to use pre-built wheels..."
    echo ""
fi

# Install packages
echo "📦 Installing required packages..."

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 14 ]; then
    echo "⚠️  Warning: Python 3.14+ detected. Some packages may not have pre-built wheels."
    echo "   Consider using Python 3.11 or 3.12 for better compatibility."
    echo ""
fi

# Try to install all packages
pip install -r requirements.txt 2>&1 | tee /tmp/install_log.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All packages installed successfully!"
    echo ""
    echo "🚀 To run the app:"
    echo "   1. Activate the virtual environment: source venv/bin/activate"
    echo "   2. Run: streamlit run app.py"
    echo ""
    echo "💡 Or use the run script: ./run.sh"
    echo ""
else
    echo ""
    echo "⚠️  Installation encountered issues. Checking what was installed..."
    
    # Check if core packages are installed
    python3 -c "import openai; import dotenv" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Core packages (openai, python-dotenv) are installed."
        echo ""
        echo "❌ Streamlit installation failed (likely due to pyarrow dependency)."
        echo ""
        echo "🔧 Solutions:"
        echo "   1. Use Python 3.11 or 3.12 (recommended):"
        echo "      python3.12 -m venv venv"
        echo "      source venv/bin/activate"
        echo "      pip install -r requirements.txt"
        echo ""
        echo "   2. See QUICK_START.md for more options"
        echo ""
    else
        echo "❌ Core packages failed to install. Please check the error messages above."
        exit 1
    fi
fi

