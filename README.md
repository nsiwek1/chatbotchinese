# 🏛️ Ancient Chinese Philosophers Chat

A beautiful Streamlit application featuring conversations with Confucius (孔子) and Mencius (孟子), two of the most influential philosophers in Chinese history. Chat with both masters side-by-side or watch them debate philosophical questions!

## ✨ Features

- **💬 Dual Chat Interface** - Talk to Confucius and Mencius simultaneously
- **📜 Debate Mode** - Watch both philosophers discuss topics together
- **🌙 Dark/Light Mode** - Toggle between beautiful themes
- **💡 Preset Questions** - Quick access to common philosophical topics
- **📥 Export Conversations** - Save as Text, Markdown, or JSON
- **⚡ Streaming Responses** - See answers appear in real-time
- **🎨 Modern UI** - Clean, elegant design with Chinese aesthetics

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

3. Set up your OpenAI API key (choose one method):

   **Method 1: Using .env file (Recommended for local)**
   ```bash
   # Create .env file in project root
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

   **Method 2: Using Streamlit secrets**
   ```bash
   # Create .streamlit/secrets.toml
   mkdir -p .streamlit
   cat > .streamlit/secrets.toml << EOF
   [openai]
   api_key = "your-api-key-here"
   EOF
   ```

   **Method 3: Environment variable**
   ```bash
   export OPENAI_API_KEY=your-api-key-here  # macOS/Linux
   # or
   set OPENAI_API_KEY=your-api-key-here  # Windows
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

