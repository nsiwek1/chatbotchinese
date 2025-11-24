import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# System prompts
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

def init_session_state():
    """Initialize all session state variables"""
    if "confucius_messages" not in st.session_state:
        st.session_state.confucius_messages = []
    if "mencius_messages" not in st.session_state:
        st.session_state.mencius_messages = []
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = init_openai()
    if "debate_messages" not in st.session_state:
        st.session_state.debate_messages = []
    if "debate_active" not in st.session_state:
        st.session_state.debate_active = False
    if "response_length" not in st.session_state:
        st.session_state.response_length = "Medium"
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

# Preset questions organized by themes
PRESET_QUESTIONS = {
    "Virtue & Character": [
        "What is the path to cultivating virtue?",
        "How can I become a better person?",
        "What is the meaning of righteousness?",
        "How do I develop moral character?"
    ],
    "Leadership & Governance": [
        "What makes a good leader?",
        "How should a ruler govern their people?",
        "What is the relationship between power and morality?",
        "How can leaders earn trust?"
    ],
    "Family & Relationships": [
        "What are the duties of a child to their parents?",
        "How should I handle conflicts with family?",
        "What is the importance of filial piety?",
        "How do I build harmonious relationships?"
    ],
    "Learning & Wisdom": [
        "What is the purpose of education?",
        "How should I approach learning?",
        "What is the difference between knowledge and wisdom?",
        "How can I cultivate self-awareness?"
    ],
    "Modern Dilemmas": [
        "How do ancient principles apply to modern life?",
        "What would you say about technology and human connection?",
        "How do I balance work and personal fulfillment?",
        "What is the role of tradition in a changing world?"
    ]
}

def get_max_tokens(length_setting: str) -> int:
    """Convert length setting to max tokens"""
    length_map = {
        "Brief": 250,
        "Medium": 500,
        "Detailed": 800
    }
    return length_map.get(length_setting, 500)

def get_response_streaming(user_message: str, system_prompt: str, messages_history: list, max_tokens: int = 500):
    """Get streaming response from OpenAI API"""
    try:
        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in messages_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})
        
        stream = st.session_state.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    
    except Exception as e:
        yield f"An error occurred: {str(e)}"

def get_response(user_message: str, system_prompt: str, messages_history: list, max_tokens: int = 500) -> str:
    """Get response from OpenAI API using specified system prompt"""
    try:
        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in messages_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})
        
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_debate_response(topic: str, previous_exchanges: list, speaker: str, other_speaker_last: str = None) -> str:
    """Get a debate response from a philosopher, considering what the other said"""
    system_prompt = CONFUCIUS_SYSTEM_PROMPT if speaker == "Confucius" else MENCIUS_SYSTEM_PROMPT
    
    try:
        messages = [{"role": "system", "content": system_prompt}]
        
        debate_context = f"\n\nYou are in a respectful philosophical dialogue with {('Mencius' if speaker == 'Confucius' else 'Confucius')}. "
        debate_context += f"A student has asked: '{topic}'. "
        
        if other_speaker_last:
            debate_context += f"\n\n{('Mencius' if speaker == 'Confucius' else 'Confucius')} just said:\n\"{other_speaker_last}\"\n\n"
            debate_context += f"Respond thoughtfully, building on or respectfully contrasting with their view. Keep your response concise (2-3 paragraphs)."
        else:
            debate_context += "Please share your initial thoughts on this matter."
        
        messages.append({"role": "user", "content": debate_context})
        
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_navbar(current_page: str = "main"):
    """Create a navigation bar at the top of the page"""
    main_active = "active" if current_page == "main" else ""
    debate_active = "active" if current_page == "debate" else ""
    
    # Create columns for navbar with theme toggle
    nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
    
    with nav_col1:
        # Theme toggle button
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        theme_label = "Dark Mode" if st.session_state.theme == "light" else "Light Mode"
        if st.button(f"{theme_icon} {theme_label}", key="theme_toggle"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()
    
    with nav_col2:
        navbar_html = f"""
        <div class="navbar">
            <a href="/" target="_self" class="nav-link {main_active}">🏛️ Main Chat</a>
            <a href="/Debate_Mode" target="_self" class="nav-link {debate_active}">📜 Debate Mode</a>
        </div>
        """
        st.markdown(navbar_html, unsafe_allow_html=True)

def show_preset_questions(philosopher_name: str):
    """Display preset questions organized by themes"""
    st.markdown("### 💡 Suggested Questions")
    
    # Create expandable sections for each theme
    for theme, questions in PRESET_QUESTIONS.items():
        with st.expander(f"📚 {theme}"):
            for question in questions:
                if st.button(question, key=f"{philosopher_name}_{question}", use_container_width=True):
                    return question
    return None

def export_conversation(messages: list, philosopher: str, format: str = "txt") -> str:
    """Export conversation in various formats"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if format == "txt":
        content = f"Conversation with {philosopher}\n"
        content += f"Exported: {timestamp}\n"
        content += "=" * 50 + "\n\n"
        
        for msg in messages:
            role = "You" if msg["role"] == "user" else philosopher
            content += f"{role}:\n{msg['content']}\n\n"
        
        return content
    
    elif format == "md":
        content = f"# Conversation with {philosopher}\n\n"
        content += f"**Exported:** {timestamp}\n\n"
        content += "---\n\n"
        
        for msg in messages:
            role = "**You**" if msg["role"] == "user" else f"**{philosopher}**"
            content += f"{role}:\n\n{msg['content']}\n\n"
        
        return content
    
    elif format == "json":
        export_data = {
            "philosopher": philosopher,
            "exported_at": timestamp,
            "messages": messages
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    return ""

def get_shared_css(theme="light"):
    """Return shared CSS styling with theme support"""
    
    # Theme colors
    if theme == "dark":
        page_bg = "#0f1419"
        bg_gradient = "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)"
        card_bg = "#1e2936"
        text_color = "#ffffff"
        text_secondary = "#d0d0d0"
        border_color = "#3a4a5c"
        hover_bg = "#2a3f5f"
        input_bg = "#1e2936"
        input_text = "#ffffff"
    else:  # light theme
        page_bg = "#f5f7fa"
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%)"
        card_bg = "white"
        text_color = "#1a1a1a"
        text_secondary = "#666"
        border_color = "#e0e0e0"
        hover_bg = "#f8f9fa"
        input_bg = "white"
        input_text = "#333"
    
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Full Page Background */
    .stApp {{
        background: {page_bg} !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        background: {page_bg} !important;
    }}
    
    [data-testid="stHeader"] {{
        background: {card_bg} !important;
    }}
    
    section[data-testid="stSidebar"] {{
        background: {card_bg} !important;
    }}
    
    /* All text elements */
    .stMarkdown, .stText, p, span, div {{
        color: {text_color} !important;
    }}
    
    /* Input fields */
    .stTextInput > div > div > input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 2px solid {border_color} !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #c17817 !important;
        box-shadow: 0 0 0 3px rgba(193, 120, 23, 0.1) !important;
        outline: none !important;
    }}
    
    .stSelectbox > div > div > div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: 2px solid {border_color} !important;
        border-radius: 8px !important;
    }}
    
    /* Chat input */
    .stChatInputContainer {{
        background-color: transparent !important;
        border-top: 1px solid {border_color} !important;
        padding: 1rem 0 !important;
    }}
    
    .stChatInput > div {{
        background-color: {input_bg} !important;
        border: 2px solid {border_color} !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }}
    
    .stChatInput input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
    }}
    
    .stChatInput input::placeholder {{
        color: {text_secondary} !important;
        opacity: 0.6 !important;
    }}
    
    .stChatInput input:focus {{
        outline: none !important;
        border: none !important;
    }}
    
    .stChatInput > div:focus-within {{
        border-color: #c17817 !important;
        box-shadow: 0 0 0 3px rgba(193, 120, 23, 0.1) !important;
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: {card_bg} !important;
    }}
    
    /* Navbar Styles */
    .navbar {{
        background: {card_bg};
        padding: 1rem 2rem;
        border-bottom: 2px solid {border_color};
        margin: -1rem -1rem 2rem -1rem;
        display: flex;
        justify-content: center;
        gap: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}
    
    .nav-link {{
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        color: {text_color};
        background: {hover_bg};
        border: 1px solid {border_color};
        transition: all 0.2s ease;
        cursor: pointer;
    }}
    
    .nav-link:hover {{
        background: #c17817;
        color: white;
        border-color: #c17817;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(193, 120, 23, 0.3);
    }}
    
    .nav-link.active {{
        background: #8b4513;
        color: white;
        border-color: #8b4513;
    }}
    
    /* Global Styles */
    .main {{
        background: {bg_gradient};
        padding: 2rem 1rem;
    }}
    
    .block-container {{
        max-width: 1400px;
        padding: 1rem 2rem;
    }}
    
    /* Hide default Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Title Section */
    .main-title {{
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: {card_bg};
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    }}
    
    .chinese-title {{
        font-family: 'Noto Serif SC', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: {text_color};
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
    }}
    
    .english-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: {text_secondary};
        font-weight: 400;
        letter-spacing: 0.02em;
    }}
    
    /* Philosopher Cards */
    .philosopher-card {{
        background: {card_bg};
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid {border_color};
    }}
    
    .philosopher-header {{
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid #f0f0f0;
    }}
    
    .philosopher-image-container {{
        flex-shrink: 0;
    }}
    
    .philosopher-image {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }}
    
    .philosopher-info {{
        flex-grow: 1;
        text-align: left;
    }}
    
    .philosopher-name {{
        font-family: 'Noto Serif SC', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.3rem;
    }}
    
    .philosopher-title {{
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 0.2rem;
    }}
    
    .philosopher-chinese-title {{
        font-family: 'Noto Serif SC', serif;
        font-size: 0.9rem;
        color: #999;
        font-weight: 400;
    }}
    
    /* Confucius specific colors */
    .confucius-card {{
        border-left: 4px solid #c17817;
    }}
    
    .confucius-card .philosopher-name {{
        color: #8b4513;
    }}
    
    .confucius-card .philosopher-image {{
        border-color: #c17817;
    }}
    
    .confucius-card .philosopher-header {{
        border-bottom-color: #f4e4d0;
    }}
    
    /* Mencius specific colors */
    .mencius-card {{
        border-left: 4px solid #4a7c59;
    }}
    
    .mencius-card .philosopher-name {{
        color: #2f5233;
    }}
    
    .mencius-card .philosopher-image {{
        border-color: #4a7c59;
    }}
    
    .mencius-card .philosopher-header {{
        border-bottom-color: #d4e8da;
    }}
    
    /* Chat Messages */
    .stChatMessage {{
        background: transparent;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
    }}
    
    .stChatMessage[data-testid*="user"] {{
        background: #f8f9fa;
        border-left: 3px solid #ddd;
    }}
    
    /* Confucius chat messages */
    .confucius-card .stChatMessage[data-testid*="assistant"] {{
        background: linear-gradient(135deg, #fef9f3 0%, #fdf5e6 100%);
        border-left: 3px solid #c17817;
    }}
    
    /* Mencius chat messages */
    .mencius-card .stChatMessage[data-testid*="assistant"] {{
        background: linear-gradient(135deg, #f3faf5 0%, #e8f5e9 100%);
        border-left: 3px solid #4a7c59;
    }}
    
    /* Buttons */
    .stButton > button {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        border: 2px solid {border_color} !important;
        background: {card_bg} !important;
        color: {text_color} !important;
        transition: all 0.2s ease !important;
    }}
    
    .stButton > button:hover {{
        background: {hover_bg} !important;
        border-color: #c17817 !important;
        color: #c17817 !important;
        box-shadow: 0 2px 8px rgba(193, 120, 23, 0.2) !important;
        transform: translateY(-1px) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}
    
    /* Download buttons */
    .stDownloadButton > button {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        border: 2px solid {border_color} !important;
        background: {card_bg} !important;
        color: {text_color} !important;
        transition: all 0.2s ease !important;
    }}
    
    .stDownloadButton > button:hover {{
        background: {hover_bg} !important;
        border-color: #c17817 !important;
        color: #c17817 !important;
        box-shadow: 0 2px 8px rgba(193, 120, 23, 0.2) !important;
    }}
    
    /* Debate Mode Styles */
    .debate-section {{
        background: {card_bg};
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid {border_color};
    }}
    
    .debate-title {{
        font-family: 'Noto Serif SC', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: {text_color};
        margin-bottom: 0.5rem;
        text-align: center;
    }}
    
    .debate-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: {text_secondary};
        text-align: center;
        margin-bottom: 1.5rem;
    }}
    
    .debate-message {{
        margin: 1rem 0;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid;
    }}
    
    .debate-message.confucius {{
        background: linear-gradient(135deg, #fef9f3 0%, #fdf5e6 100%);
        border-left-color: #c17817;
    }}
    
    .debate-message.mencius {{
        background: linear-gradient(135deg, #f3faf5 0%, #e8f5e9 100%);
        border-left-color: #4a7c59;
    }}
    
    .debate-message.topic {{
        background: linear-gradient(135deg, #f0f4ff 0%, #e6eeff 100%);
        border-left-color: #4a6fa5;
        text-align: center;
    }}
    
    .speaker-label {{
        font-family: 'Noto Serif SC', serif;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }}
    
    .speaker-label.confucius {{
        color: #8b4513;
    }}
    
    .speaker-label.mencius {{
        color: #2f5233;
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #f1f1f1;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: #ccc;
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: #999;
    }}
    </style>
    """

