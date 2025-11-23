import streamlit as st
from openai import OpenAI
import os
from typing import List, Dict
from dotenv import load_dotenv
from PIL import Image

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

# System prompt for Mencius
MENCIUS_SYSTEM_PROMPT = """
You are to speak and reason as Mencius (Mengzi), grounded in the teachings of the Mencius (Mengzi). Stay fully in character at all times.

CORE PERSONA
- Voice & style: eloquent, argumentative, passionate. Use extended analogies and parables. Speak with conviction about human goodness and moral cultivation.
- Moral center: Innate Goodness of Human Nature (Ren), Righteousness (Yi), Wisdom (Zhi), Propriety (Li), Humaneness/Benevolence. Emphasis on the "Four Beginnings" (compassion, shame, deference, right/wrong).
- Method: use vivid analogies (the child at the well, Ox Mountain), argue for the inherent goodness of human nature, emphasize moral cultivation and the role of environment.

DEFAULT RULES
1. Be eloquent but clear—2–4 paragraphs. Use analogies and parables when appropriate.
2. Anchor guidance in the Mencius. Reference key concepts: the Four Beginnings, the distinction between humans and animals, the role of qi (vital energy).
3. Emphasize that human nature is inherently good; evil comes from losing one's original heart-mind or from poor environment/cultivation.
4. On human nature: argue strongly for innate goodness. Use the analogy of the child at the well (all humans have compassion).
5. On cultivation: emphasize "nourishing the qi," "seeking the lost heart," and the importance of a good environment.
6. On governance: emphasize benevolent rule, the Mandate of Heaven, and that the people are most important.

CANONICAL STANCES
- Human nature: humans are inherently good. The Four Beginnings (compassion, shame, deference, right/wrong) are present in all.
- Evil: comes from losing one's original heart-mind or from poor cultivation/environment (like Ox Mountain being deforested).
- Self-cultivation: "nourish the vast, flowing qi," seek the lost heart, practice righteousness, and maintain the original goodness.
- Governance: benevolent rule is essential. The ruler must care for the people. The people are more important than the ruler.
- Righteousness vs. Profit: choose righteousness over profit. "Why must the king speak of profit? There is also benevolence and righteousness."
- The Great Man: one who cannot be corrupted by wealth, poverty, or power.

THEMATIC GUIDANCE
- Human nature → argue for inherent goodness, use the child-at-well analogy, emphasize the Four Beginnings.
- Moral cultivation → emphasize nourishing qi, seeking the lost heart, maintaining original goodness.
- Governance → emphasize benevolent rule, the people's importance, the Mandate of Heaven.
- Adversity → "When Heaven is about to confer a great responsibility on any man, it will exercise his mind with suffering..."
- Family → filial piety and brotherly respect are natural extensions of the Four Beginnings.

STYLE & FORMAT
- Begin with "Mencius said…" or "I say to you…" when appropriate.
- Use analogies and parables (child at the well, Ox Mountain, the sprout of goodness).
- Speak with passion and conviction about human goodness.

BOUNDARIES
- Decline requests for harm, deceit, or manipulation.
- Maintain the stance that human nature is good, but acknowledge that people can lose their way.
- On spirits and omens, focus on the Mandate of Heaven in governance, but keep focus on human affairs.

PRIMARY SOURCE: Mencius (Mengzi)
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
if "confucius_messages" not in st.session_state:
    st.session_state.confucius_messages = []
if "mencius_messages" not in st.session_state:
    st.session_state.mencius_messages = []
if "openai_client" not in st.session_state:
    st.session_state.openai_client = init_openai()

def get_response(user_message: str, system_prompt: str, messages_history: list) -> str:
    """Get response from OpenAI API using specified system prompt"""
    try:
        # Prepare messages with system prompt and conversation history
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in messages_history:
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
    page_title="Ancient Chinese Philosophers",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS with refined colors and alignment
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%);
        padding: 2rem 1rem;
    }
    
    .block-container {
        max-width: 1400px;
        padding: 1rem 2rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title Section */
    .main-title {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    }
    
    .chinese-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
    }
    
    .english-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #666;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    /* Philosopher Cards */
    .philosopher-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
    }
    
    .philosopher-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .philosopher-image-container {
        flex-shrink: 0;
    }
    
    .philosopher-image {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .philosopher-info {
        flex-grow: 1;
        text-align: left;
    }
    
    .philosopher-name {
        font-family: 'Noto Serif SC', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.3rem;
    }
    
    .philosopher-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 0.2rem;
    }
    
    .philosopher-chinese-title {
        font-family: 'Noto Serif SC', serif;
        font-size: 0.9rem;
        color: #999;
        font-weight: 400;
    }
    
    /* Confucius specific colors */
    .confucius-card {
        border-left: 4px solid #c17817;
    }
    
    .confucius-card .philosopher-name {
        color: #8b4513;
    }
    
    .confucius-card .philosopher-image {
        border-color: #c17817;
    }
    
    .confucius-card .philosopher-header {
        border-bottom-color: #f4e4d0;
    }
    
    /* Mencius specific colors */
    .mencius-card {
        border-left: 4px solid #4a7c59;
    }
    
    .mencius-card .philosopher-name {
        color: #2f5233;
    }
    
    .mencius-card .philosopher-image {
        border-color: #4a7c59;
    }
    
    .mencius-card .philosopher-header {
        border-bottom-color: #d4e8da;
    }
    
    /* Chat Container */
    .stChatFloatingInputContainer {
        background: white;
        border-top: 1px solid #e0e0e0;
        padding: 1rem;
    }
    
    .stChatInput > div {
        border-radius: 12px;
    }
    
    .stChatInput input {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 0.75rem 1rem;
    }
    
    .stChatInput input:focus {
        border-color: #c17817;
        box-shadow: 0 0 0 3px rgba(193, 120, 23, 0.1);
    }
    
    /* Confucius chat input styling */
    .confucius-card .stChatInput input:focus {
        border-color: #c17817;
        box-shadow: 0 0 0 3px rgba(193, 120, 23, 0.1);
    }
    
    /* Mencius chat input styling */
    .mencius-card .stChatInput input:focus {
        border-color: #4a7c59;
        box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.1);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: transparent;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
    }
    
    .stChatMessage[data-testid*="user"] {
        background: #f8f9fa;
        border-left: 3px solid #ddd;
    }
    
    /* Confucius chat messages */
    .confucius-card .stChatMessage[data-testid*="assistant"] {
        background: linear-gradient(135deg, #fef9f3 0%, #fdf5e6 100%);
        border-left: 3px solid #c17817;
    }
    
    /* Mencius chat messages */
    .mencius-card .stChatMessage[data-testid*="assistant"] {
        background: linear-gradient(135deg, #f3faf5 0%, #e8f5e9 100%);
        border-left: 3px solid #4a7c59;
    }
    
    /* Buttons */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        border: 1px solid #e0e0e0;
        background: white;
        color: #333;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #f8f9fa;
        border-color: #c17817;
        color: #c17817;
        box-shadow: 0 2px 8px rgba(193, 120, 23, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(1px);
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e0e0e0;
    }
    
    .sidebar-content {
        font-family: 'Inter', sans-serif;
        color: #333;
        line-height: 1.6;
    }
    
    /* Container heights */
    .element-container:has(.stChatMessage) {
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #999;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("""
    <div class='main-title'>
        <div class='chinese-title'>古代哲学家对话</div>
        <div class='english-subtitle'>Ancient Chinese Philosophers Dialogue</div>
    </div>
""", unsafe_allow_html=True)

# Create two columns for side-by-side chatbots with equal spacing
col1, col2 = st.columns([1, 1], gap="large")

# Confucius Chatbot (Left Column)
with col1:
    # Header with image and info side by side
    col_img, col_info = st.columns([1, 3], gap="medium")
    with col_img:
        try:
            st.image("confucius-2.png", width=100)
        except:
            pass
    
    with col_info:
        st.markdown("""
            <div class="philosopher-info" style="padding-top: 0.5rem;">
                <div class="philosopher-name">孔子 Confucius</div>
                <div class="philosopher-title">The Master of Practical Wisdom</div>
                <div class="philosopher-chinese-title">至聖先師</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    
    # Chat container
    confucius_container = st.container(height=450)
    with confucius_container:
        for message in st.session_state.confucius_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    # Chat input
    confucius_input = st.chat_input("Ask Confucius a question...", key="confucius_input")
    
    if confucius_input:
        st.session_state.confucius_messages.append({"role": "user", "content": confucius_input})
        
        with confucius_container:
            with st.chat_message("user"):
                st.write(confucius_input)
        
        with confucius_container:
            with st.chat_message("assistant"):
                with st.spinner("Contemplating..."):
                    response = get_response(confucius_input, CONFUCIUS_SYSTEM_PROMPT, st.session_state.confucius_messages[:-1])
                    st.write(response)
        
        st.session_state.confucius_messages.append({"role": "assistant", "content": response})
        st.rerun()

# Mencius Chatbot (Right Column)
with col2:
    
    # Header with image and info side by side
    col_img, col_info = st.columns([1, 3], gap="medium")
    with col_img:
        try:
            st.image("mencius.png", width=100)
        except:
            pass
    
    with col_info:
        st.markdown("""
            <div class="philosopher-info" style="padding-top: 0.5rem;">
                <div class="philosopher-name">孟子 Mencius</div>
                <div class="philosopher-title">The Philosopher of Human Goodness</div>
                <div class="philosopher-chinese-title">亞聖</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    
    # Chat container
    mencius_container = st.container(height=450)
    with mencius_container:
        for message in st.session_state.mencius_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(message["content"])
    
    # Chat input
    mencius_input = st.chat_input("Ask Mencius a question...", key="mencius_input")
    
    if mencius_input:
        st.session_state.mencius_messages.append({"role": "user", "content": mencius_input})
        
        with mencius_container:
            with st.chat_message("user"):
                st.write(mencius_input)
        
        with mencius_container:
            with st.chat_message("assistant"):
                with st.spinner("Reflecting..."):
                    response = get_response(mencius_input, MENCIUS_SYSTEM_PROMPT, st.session_state.mencius_messages[:-1])
                    st.write(response)
        
        st.session_state.mencius_messages.append({"role": "assistant", "content": response})
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### Settings")
    
    st.markdown("---")
    
    if st.button("Clear Confucius Chat", use_container_width=True):
        st.session_state.confucius_messages = []
        st.rerun()
    
    if st.button("Clear Mencius Chat", use_container_width=True):
        st.session_state.mencius_messages = []
        st.rerun()
    
    if st.button("Clear Both Chats", use_container_width=True):
        st.session_state.confucius_messages = []
        st.session_state.mencius_messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
        <div class='sidebar-content'>
        <p><strong>About</strong></p>
        <p style='font-size: 0.9rem; line-height: 1.6;'>
        Compare the teachings of two influential Chinese philosophers who shaped Eastern thought for millennia.
        </p>
        <p style='font-size: 0.85rem; margin-top: 1rem;'>
        <strong>Confucius (孔子)</strong><br>
        551-479 BCE<br>
        Focus: Ritual, propriety, and moral cultivation
        </p>
        <p style='font-size: 0.85rem; margin-top: 1rem;'>
        <strong>Mencius (孟子)</strong><br>
        372-289 BCE<br>
        Focus: Inherent human goodness and moral nature
        </p>
        </div>
    """, unsafe_allow_html=True)
