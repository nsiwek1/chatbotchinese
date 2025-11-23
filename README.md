# Confucius Chatbot

A beautiful Streamlit chatbot application that uses OpenAI's API to generate answers in the style of Confucius, based on the teachings of the Analects.

## Features

- Clean, modern UI with a chat interface
- Responses in the authentic style of Confucius
- Conversation history maintained during the session
- Easy to use and navigate

## Quick Setup

### ⚠️ Important: Python Version

**Python 3.11 or 3.12 is recommended** for best package compatibility. Python 3.14+ may have issues with pyarrow (a streamlit dependency).

### Option 1: Automated Setup (Recommended)

**On macOS/Linux:**
```bash
./setup.sh
./run.sh
```

**On Windows:**
```cmd
setup.bat
run.bat
```

**If you have Python 3.14+ and encounter pyarrow issues:**
```bash
# Use Python 3.12 instead
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Option 2: Manual Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root and add:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - Or set it as an environment variable:
     ```bash
     export OPENAI_API_KEY=your_api_key_here  # On Windows: set OPENAI_API_KEY=your_api_key_here
     ```
   - Or use Streamlit secrets (create `.streamlit/secrets.toml`):
     ```
     OPENAI_API_KEY = "your_api_key_here"
     ```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your question in the chat input at the bottom
2. The chatbot will respond in the style of Confucius
3. Use the sidebar to clear chat history if needed

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection

## Troubleshooting

If you encounter package installation issues:

**"cmake not found" error:**
- This happens when pyarrow needs to build from source (common with very new Python versions)
- Install cmake: `brew install cmake` (macOS) or `sudo apt-get install cmake` (Linux)
- Then run the setup script again

**Other issues:**
- Make sure you're using a virtual environment
- Try upgrading pip: `pip install --upgrade pip`
- On macOS, if you see "externally-managed-environment" error, use the virtual environment setup
- If pyarrow still fails, try: `pip install pyarrow --only-binary :all:` first, then install other packages

