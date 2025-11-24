import streamlit as st
import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    init_session_state, 
    get_debate_response, 
    get_shared_css,
    export_conversation,
    create_navbar
)

# Initialize session state
init_session_state()

# Apply page background color based on theme
page_bg_color = "#0f1419" if st.session_state.theme == "dark" else "#f5f7fa"
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {page_bg_color};
    }}
    </style>
""", unsafe_allow_html=True)

# Apply shared CSS with current theme
st.markdown(get_shared_css(st.session_state.theme), unsafe_allow_html=True)

# Navigation Bar
create_navbar("debate")

# Title Section
st.markdown("""
    <div class='main-title'>
        <div class='chinese-title'>📜 哲学辩论 Philosophical Debate</div>
        <div class='english-subtitle'>Watch Confucius and Mencius discuss profound questions</div>
    </div>
""", unsafe_allow_html=True)

# Debate Section
st.markdown("""
    <div class='debate-section'>
        <div class='debate-subtitle'>Enter a philosophical question and watch both masters engage in thoughtful dialogue</div>
    </div>
""", unsafe_allow_html=True)

debate_col1, debate_col2, debate_col3 = st.columns([1, 2, 1])

with debate_col2:
    debate_topic = st.text_input(
        "Enter a topic for debate:", 
        placeholder="e.g., What is the best way to cultivate virtue?",
        key="debate_topic_input"
    )
    
    debate_btn_col1, debate_btn_col2, debate_btn_col3 = st.columns([1, 1, 1])
    
    with debate_btn_col1:
        start_debate = st.button("🎭 Start Debate", use_container_width=True)
    
    with debate_btn_col2:
        if st.session_state.debate_active and len(st.session_state.debate_messages) > 0:
            continue_debate = st.button("➡️ Continue", use_container_width=True)
        else:
            continue_debate = False
    
    with debate_btn_col3:
        clear_debate = st.button("🗑️ Clear Debate", use_container_width=True)

# Export controls
if st.session_state.debate_messages and len(st.session_state.debate_messages) > 1:
    st.markdown("---")
    export_col1, export_col2, export_col3, export_col4, export_col5 = st.columns([1, 1, 1, 1, 1])
    
    with export_col2:
        export_format = st.selectbox("Export format:", ["Text (.txt)", "Markdown (.md)", "JSON (.json)"], key="debate_export_format")
    
    with export_col3:
        format_map = {"Text (.txt)": "txt", "Markdown (.md)": "md", "JSON (.json)": "json"}
        selected_format = format_map[export_format]
        
        # Create debate export content
        debate_export = f"Philosophical Debate\nTopic: {st.session_state.debate_messages[0]['content']}\n\n"
        for msg in st.session_state.debate_messages[1:]:
            if msg.get("speaker"):
                debate_export += f"\n{msg['speaker']}:\n{msg['content']}\n"
        
        st.download_button(
            label=f"📥 Export Debate",
            data=debate_export,
            file_name=f"debate_{st.session_state.debate_messages[0]['content'][:30].replace(' ', '_')}.{selected_format}",
            mime="text/plain",
            use_container_width=True
        )

# Display debate messages
if st.session_state.debate_messages:
    st.markdown("---")
    debate_container = st.container()
    with debate_container:
        for msg in st.session_state.debate_messages:
            if msg["type"] == "topic":
                st.markdown(f"""
                    <div class='debate-message topic'>
                        <div style='font-weight: 600; font-size: 1.1rem;'>📖 Topic for Discussion</div>
                        <div style='margin-top: 0.5rem; font-size: 1rem;'>{msg["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                speaker_class = "confucius" if msg["speaker"] == "Confucius" else "mencius"
                speaker_chinese = "孔子" if msg["speaker"] == "Confucius" else "孟子"
                st.markdown(f"""
                    <div class='debate-message {speaker_class}'>
                        <div class='speaker-label {speaker_class}'>{speaker_chinese} {msg["speaker"]}</div>
                        <div>{msg["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)

# Handle debate actions
if start_debate and debate_topic:
    st.session_state.debate_messages = [{"type": "topic", "content": debate_topic}]
    st.session_state.debate_active = True
    
    # Get initial responses from both philosophers
    with st.spinner("Confucius is contemplating..."):
        confucius_response = get_debate_response(debate_topic, [], "Confucius")
        st.session_state.debate_messages.append({
            "speaker": "Confucius",
            "content": confucius_response,
            "type": "response"
        })
    
    with st.spinner("Mencius is reflecting..."):
        mencius_response = get_debate_response(debate_topic, [], "Mencius", confucius_response)
        st.session_state.debate_messages.append({
            "speaker": "Mencius",
            "content": mencius_response,
            "type": "response"
        })
    
    st.rerun()

elif continue_debate and st.session_state.debate_active:
    # Get the last response from Mencius
    last_mencius = [msg for msg in st.session_state.debate_messages if msg.get("speaker") == "Mencius"][-1]["content"]
    topic = st.session_state.debate_messages[0]["content"]
    
    # Confucius responds to Mencius
    with st.spinner("Confucius is responding..."):
        confucius_response = get_debate_response(topic, st.session_state.debate_messages, "Confucius", last_mencius)
        st.session_state.debate_messages.append({
            "speaker": "Confucius",
            "content": confucius_response,
            "type": "response"
        })
    
    # Mencius responds to Confucius
    with st.spinner("Mencius is responding..."):
        mencius_response = get_debate_response(topic, st.session_state.debate_messages, "Mencius", confucius_response)
        st.session_state.debate_messages.append({
            "speaker": "Mencius",
            "content": mencius_response,
            "type": "response"
        })
    
    st.rerun()

elif clear_debate:
    st.session_state.debate_messages = []
    st.session_state.debate_active = False
    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 📜 Debate Settings")
    
    st.markdown("""
        <div style='font-size: 0.9rem; line-height: 1.6; color: #666; margin-top: 1rem;'>
        <p><strong>How to use:</strong></p>
        <ol>
        <li>Enter a philosophical question or topic</li>
        <li>Click "Start Debate" to begin</li>
        <li>Watch as both philosophers share their perspectives</li>
        <li>Click "Continue" to deepen the discussion</li>
        <li>Export your favorite debates for later reference</li>
        </ol>
        
        <p style='margin-top: 1rem;'><strong>Example topics:</strong></p>
        <ul>
        <li>What is the nature of human goodness?</li>
        <li>How should a leader govern?</li>
        <li>What is the path to self-cultivation?</li>
        <li>How do we resolve moral conflicts?</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div style='font-size: 0.9rem; line-height: 1.6; color: #666; text-align: center;'>
        <p>💡 <strong>Tip:</strong> Use the navigation bar at the top to switch between Main Chat and Debate Mode.</p>
        </div>
    """, unsafe_allow_html=True)

