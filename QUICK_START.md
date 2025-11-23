# Quick Start Guide

## Python Version Issue

You're using Python 3.14, which is very new. Some packages (like pyarrow, required by streamlit) don't have pre-built wheels yet.

## Solution Options

### Option 1: Use Python 3.11 or 3.12 (Recommended)

Create a new virtual environment with an older Python version:

```bash
# Install Python 3.12 if you don't have it
brew install python@3.12

# Create venv with Python 3.12
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Option 2: Install packages without pyarrow dependency

The core packages (openai, python-dotenv) are already installed. You can run a simplified version, or wait for pyarrow wheels for Python 3.14.

### Option 3: Manual Installation

Try installing streamlit with a workaround:

```bash
source venv/bin/activate
pip install --no-deps streamlit
pip install altair blinker cachetools click numpy pandas pillow protobuf requests tenacity toml typing-extensions gitpython pydeck tornado jinja2 jsonschema
```

Note: This may not work perfectly as pyarrow is a core dependency.

## Current Status

✅ OpenAI package installed
✅ python-dotenv installed
❌ Streamlit installation blocked by pyarrow (needs Python 3.11/3.12)

## Recommended Action

Use Python 3.12 for best compatibility with all packages.

