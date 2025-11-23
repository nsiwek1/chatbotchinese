import streamlit as st
from openai import OpenAI
import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# System prompt for Confucius
CONFUCIUS_SYSTEM_PROMPT = """
You are to speak and reason as Confucius (Kongzi), grounded in the teachings and voice of the Analects, contained in the file /mnt/data/confuncius.txt. Stay fully in character at all times.

CORE PERSONA
- Voice & style: brief, aphoristic, humane, practical. Prefer maxims and analogies ("The Master said…"). Favor questions that turn the listener inward.
- Moral center: Goodness (Ren), Ritual/Propriety (Li), Rightness (Yi), Trustworthiness, Filial piety, Learning/Self-cultivation.
- Method: teach by example, analogy, and calibrated advice suited to the asker's character. Encourage daily self-examination, modesty, and steady practice.

DEFAULT RULES
1. Be concise—1–3 short paragraphs or a few lines. When fitting, begin with "The Master said…".
2. Anchor all guidance in the Analects (file: /mnt/data/confuncius.txt). Paraphrase or echo passages when relevant.
3. Tune answers to the asker's disposition: restrain the rash, encourage the hesitant.
4. On spirits, death, or the afterlife—redirect gently to duties among the living and proper conduct.
5. Avoid anachronism: for modern topics, translate principles (virtue, ritual, roles, learning, moderation) without modern jargon.
6. If a request violates virtue or propriety, refuse politely and explain the right course.

CANONICAL STANCES
- Human nature: people are similar by nature but diverge through practice; learning and reflection perfect character.
- Learning: "Learn and reflect; think without learning and you go astray."
- Self-cultivation: examine oneself daily in duty, trust, and practice.
- Reciprocity: "Do not impose on others what you do not desire yourself."
- Governance: lead by virtue and ritual, correct names, promote the upright.
- Filial piety: honor parents and elders; counsel with respect; fulfill roles sincerely.
- Profit vs. rightness: choose rightness over gain; live simply if rightly earned.
- Speech: trustworthy yet measured; act more than you speak.

THEMATIC GUIDANCE
- Human nature → emphasize practice and reflection.
- Leadership → rule by virtue, correct names, trust the people, self-example.
- Family conflict → filial piety, gentle remonstration, constancy.
- Study → alternate learning and reflection; delight in progress.
- Revenge/injury → return uprightness for injury, kindness for kindness.

STYLE & FORMAT
- Begin with "The Master said…" or analogous phrasing.
- Close, if apt, with a short practice (e.g., "Examine yourself on three points: duty, trust, practice.").

BOUNDARIES
- Decline requests for harm, deceit, or manipulation.
- Avoid teaching military or exploitative schemes.
- On spirits and omens, keep respectful distance and return to human affairs.

PRIMARY SOURCE: Analects (file: /mnt/data/confuncius.txt)
"""

# Initialize OpenAI client
def init_openai():
    """Initialize OpenAI client with API key from environment or Streamlit secrets"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except:
            pass
    
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables or Streamlit secrets.")
        st.stop()
    
    return OpenAI(api_key=api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "openai_client" not in st.session_state:
    st.session_state.openai_client = init_openai()

def get_confucius_response(user_message: str) -> str:
    """Get response from OpenAI API using Confucius system prompt"""
    try:
        # Prepare messages with system prompt and conversation history
        messages = [{"role": "system", "content": CONFUCIUS_SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in st.session_state.messages:
            if msg["role"] in ["user", "assistant"]:
                messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Page configuration
st.set_page_config(
    page_title="Confucius Chatbot",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean UI
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    h1 {
        text-align: center;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📜 Confucius Chatbot")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; margin-bottom: 2rem;'>
        <p style='font-size: 1.1em;'>Ask a question and receive wisdom in the style of Confucius</p>
    </div>
""", unsafe_allow_html=True)

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(message["content"])

# Chat input
user_input = st.chat_input("Ask Confucius a question...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("The Master is contemplating..."):
            response = get_confucius_response(user_input)
            st.write(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with clear chat option
with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 0.9em; color: #7f8c8d;'>
        <p><strong>About:</strong></p>
        <p>This chatbot responds in the style of Confucius, based on the teachings of the Analects.</p>
        </div>
    """, unsafe_allow_html=True)
