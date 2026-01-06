# ============================================================================
# APPLICATION: AI Neural Translator Pro
# AUTHOR: CodeAlpha
# DESCRIPTION: Professional translation dashboard with text analytics (Word/Char count),
#              TTS synthesis, and modern UI design.
# ============================================================================

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import datetime

# ============================================================================
# 1. PAGE CONFIGURATION & STYLING
# ============================================================================

st.set_page_config(
    page_title="AI Translator Pro",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS for a "Glassmorphism" look
st.markdown("""
<style>
    /* Background & Main Theme */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Container Cards Styling */
    .css-card {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Input/Text Area Styling */
    .stTextArea textarea {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 10px;
        font-size: 16px;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        color: #2c3e50;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 18px;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. HELPER FUNCTIONS
# ============================================================================

LANGUAGES = {
    'Auto-detect': 'auto', 'Arabic': 'ar', 'English': 'en', 'French': 'fr', 
    'German': 'de', 'Spanish': 'es', 'Italian': 'it', 'Japanese': 'ja', 
    'Russian': 'ru', 'Turkish': 'tr', 'Chinese': 'zh-CN'
}

def get_text_metrics(text):
    """Calculate character and word count."""
    if not text:
        return 0, 0
    return len(text), len(text.split())

def text_to_speech(text, lang):
    """Generate TTS audio bytes."""
    try:
        if lang == 'auto': lang = 'en' # Fallback
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        return fp
    except:
        return None

# ============================================================================
# 3. MAIN DASHBOARD UI
# ============================================================================

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔮 AI Neural Translator Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Advanced Translation • Text Analytics • Speech Synthesis</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Main Interface ---
col1, col2 = st.columns([1, 1], gap="large")

# === LEFT COLUMN: INPUT ===
with col1:
    st.markdown("### 📝 Source Input")
    
    # Language Selector
    src_lang = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0)
    
    # Input Area
    source_text = st.text_area("Type your text here...", height=250, key="source_input")
    
    # 📊 Live Analytics (Counters)
    char_count, word_count = get_text_metrics(source_text)
    
    # Display Metrics in a neat row
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Characters", char_count)
    with m2: st.metric("Words", word_count)
    with m3: st.metric("Language", src_lang)

# === RIGHT COLUMN: OUTPUT ===
with col2:
    st.markdown("### 🎯 Translation Output")
    
    # Language Selector (Default to Arabic)
    tgt_lang = st.selectbox("Target Language", list(LANGUAGES.keys())[1:], index=0) # Skip Auto
    
    # Placeholder for result
    result_box = st.empty()
    audio_box = st.empty()

# === ACTION BAR ===
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])

with btn_col2:
    translate_btn = st.button("🚀 Translate & Analyze")

# ============================================================================
# 4. LOGIC ENGINE
# ============================================================================

if translate_btn:
    if source_text.strip():
        with st.spinner("Processing... Neural Engine Active"):
            try:
                # 1. Prepare Codes
                src_code = LANGUAGES[src_lang]
                tgt_code = LANGUAGES[tgt_lang]
                
                # 2. Translate
                translator = GoogleTranslator(source=src_code, target=tgt_code)
                translated_text = translator.translate(source_text)
                
                # 3. Render Output
                with col2:
                    st.success(translated_text)
                    
                    # 4. Generate Audio
                    audio_data = text_to_speech(translated_text, tgt_code)
                    if audio_data:
                        st.markdown("**🔊 Pronunciation:**")
                        st.audio(audio_data, format='audio/mp3')
                        
            except Exception as e:
                st.error(f"System Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter text to translate.")

# ============================================================================
# 5. FOOTER
# ============================================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #95a5a6; font-size: 12px;'>
        © 2026 AI Translator Pro | Powered by Deep Learning
    </div>
    """, 
    unsafe_allow_html=True
)
