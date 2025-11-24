import streamlit as st
from PIL import Image
from utils import (
    init_session_state,
    get_response_streaming,
    get_shared_css,
    export_conversation,
    create_navbar,
    show_preset_questions,
    CONFUCIUS_SYSTEM_PROMPT,
    MENCIUS_SYSTEM_PROMPT
)

# Initialize session state
init_session_state()

# Page configuration
st.set_page_config(
    page_title="Ancient Chinese Philosophers",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
create_navbar("main")

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
            st.image("confucius-2.png", width=70)
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
    
    # Export controls for Confucius
    if st.session_state.confucius_messages:
        export_col1, export_col2 = st.columns([2, 1])
        with export_col1:
            export_format_c = st.selectbox(
                "Export format:", 
                ["Text (.txt)", "Markdown (.md)", "JSON (.json)"], 
                key="confucius_export_format",
                label_visibility="collapsed"
            )
        with export_col2:
            format_map = {"Text (.txt)": "txt", "Markdown (.md)": "md", "JSON (.json)": "json"}
            selected_format = format_map[export_format_c]
            export_content = export_conversation(st.session_state.confucius_messages, "Confucius", selected_format)
            
            st.download_button(
                label="📥 Export",
                data=export_content,
                file_name=f"confucius_conversation.{selected_format}",
                mime="text/plain" if selected_format != "json" else "application/json",
                use_container_width=True
            )
    
    # Preset questions
    preset_question_c = show_preset_questions("confucius")
    
    # Chat container
    confucius_container = st.container(height=400)
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
    
    # Use preset question if clicked
    if preset_question_c:
        confucius_input = preset_question_c
    
    if confucius_input:
        st.session_state.confucius_messages.append({"role": "user", "content": confucius_input})
        
        with confucius_container:
            with st.chat_message("user"):
                st.write(confucius_input)
        
        max_tokens = 500  # Medium length response
        
        with confucius_container:
            with st.chat_message("assistant"):
                with st.spinner("Contemplating..."):
                    # Streaming response
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    for chunk in get_response_streaming(
                        confucius_input, 
                        CONFUCIUS_SYSTEM_PROMPT, 
                        st.session_state.confucius_messages[:-1],
                        max_tokens
                    ):
                        full_response += chunk
                        response_placeholder.write(full_response)
        
        st.session_state.confucius_messages.append({"role": "assistant", "content": full_response})
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
    
    # Export controls for Mencius
    if st.session_state.mencius_messages:
        export_col1, export_col2 = st.columns([2, 1])
        with export_col1:
            export_format_m = st.selectbox(
                "Export format:", 
                ["Text (.txt)", "Markdown (.md)", "JSON (.json)"], 
                key="mencius_export_format",
                label_visibility="collapsed"
            )
        with export_col2:
            format_map = {"Text (.txt)": "txt", "Markdown (.md)": "md", "JSON (.json)": "json"}
            selected_format = format_map[export_format_m]
            export_content = export_conversation(st.session_state.mencius_messages, "Mencius", selected_format)
            
            st.download_button(
                label="📥 Export",
                data=export_content,
                file_name=f"mencius_conversation.{selected_format}",
                mime="text/plain" if selected_format != "json" else "application/json",
                use_container_width=True
            )
    
    # Preset questions
    preset_question_m = show_preset_questions("mencius")
    
    # Chat container
    mencius_container = st.container(height=400)
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
    
    # Use preset question if clicked
    if preset_question_m:
        mencius_input = preset_question_m
    
    if mencius_input:
        st.session_state.mencius_messages.append({"role": "user", "content": mencius_input})
        
        with mencius_container:
            with st.chat_message("user"):
                st.write(mencius_input)
        
        max_tokens = 500  # Medium length response
        
        with mencius_container:
            with st.chat_message("assistant"):
                with st.spinner("Reflecting..."):
                    # Streaming response
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    for chunk in get_response_streaming(
                        mencius_input, 
                        MENCIUS_SYSTEM_PROMPT, 
                        st.session_state.mencius_messages[:-1],
                        max_tokens
                    ):
                        full_response += chunk
                        response_placeholder.write(full_response)
        
        st.session_state.mencius_messages.append({"role": "assistant", "content": full_response})
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("### 🗑️ Clear Conversations")
    
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
