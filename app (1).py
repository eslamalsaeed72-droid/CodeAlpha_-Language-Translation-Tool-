
# ============================================================================
# SECTION 1: IMPORTS - Required Libraries and Dependencies
# ============================================================================

import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from datetime import datetime

# ============================================================================
# SECTION 2: PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="🌍 Advanced Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SECTION 3: CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .main { padding: 2rem; }
    .stButton button {
        background-color: #667eea;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #764ba2;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stExpander {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SECTION 4: SESSION STATE INITIALIZATION
# ============================================================================

if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

if 'character_count' not in st.session_state:
    st.session_state.character_count = 0

# ============================================================================
# SECTION 5: LANGUAGE DICTIONARY
# ============================================================================

LANGUAGES = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali',
    'ca': 'Catalan', 'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Traditional)',
    'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek',
    'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'fa': 'Persian',
    'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'he': 'Hebrew',
    'hi': 'Hindi', 'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian',
    'ja': 'Japanese', 'kn': 'Kannada', 'ko': 'Korean', 'lt': 'Lithuanian',
    'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali', 'nl': 'Dutch',
    'no': 'Norwegian', 'pa': 'Punjabi', 'pl': 'Polish', 'pt': 'Portuguese',
    'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian',
    'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish', 'sw': 'Swahili',
    'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Tagalog',
    'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese',
    'yo': 'Yoruba', 'zu': 'Zulu'
}

# ============================================================================
# SECTION 7: TRANSLATION FUNCTION - Fixed using deep-translator
# ============================================================================

def translate_text(text, src_lang, dest_lang):
    """
    Execute translation using deep-translator (Synchronous & Stable).
    """
    try:
        # Handle auto-detect
        if src_lang is None or src_lang == 'auto':
            src_lang = 'auto'
        
        # deep-translator handles synchronous calls perfectly
        translator = GoogleTranslator(source=src_lang, target=dest_lang)
        return translator.translate(text)
    
    except Exception as e:
        st.error(f"❌ Translation API Error: {str(e)}")
        return None

# ============================================================================
# SECTION 8: SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Settings & Info")
    st.markdown("---")
    st.markdown("""
    **About This App:**
    - 🌐 Powered by Deep Translator
    - ⚡ No Async Errors
    - 📊 Track translation history
    """)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Translations", len(st.session_state.translation_history))
    with col2:
        st.metric("Chars Translated", st.session_state.character_count)
    st.markdown("---")
    st.markdown("Built with Python 🐍 & Streamlit 🎨")

# ============================================================================
# SECTION 9: HEADER
# ============================================================================

st.markdown("# 🌍 Advanced Language Translator")
st.markdown("### Translate text instantly with high accuracy!")
st.markdown("---")

# ============================================================================
# SECTION 10: MAIN CONTENT AREA
# ============================================================================

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Input Text")
    source_text = st.text_area(
        "Enter text to translate:",
        placeholder="Type or paste your text here...",
        height=200,
        key="source_text"
    )

with col2:
    st.markdown("### 🎯 Language Settings")
    
    auto_detect = st.checkbox("🔍 Auto-detect source language", value=True)
    
    if auto_detect:
        st.info("Source language will be detected automatically")
        source_lang = 'auto'
        source_lang_display = "Auto-detect"
    else:
        source_lang_name = st.selectbox(
            "Select source language:",
            options=list(LANGUAGES.values()),
            index=list(LANGUAGES.values()).index('English')
        )
        source_lang = [k for k, v in LANGUAGES.items() if v == source_lang_name][0]
        source_lang_display = source_lang_name
    
    st.markdown("---")
    
    target_lang_name = st.selectbox(
        "Select target language:",
        options=list(LANGUAGES.values()),
        index=list(LANGUAGES.values()).index('Arabic')
    )
    target_lang = [k for k, v in LANGUAGES.items() if v == target_lang_name][0]

# ============================================================================
# SECTION 11: TRANSLATE BUTTON & LOGIC
# ============================================================================

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    translate_btn = st.button("🚀 Translate", use_container_width=True)

if translate_btn:
    if source_text.strip():
        with st.spinner("⏳ Translating..."):
            
            # 1. Detect language for display purposes (Optional)
            if auto_detect:
                try:
                    DetectorFactory.seed = 0
                    detected_code = detect(source_text)
                    source_lang_display = LANGUAGES.get(detected_code, detected_code)
                except:
                    source_lang_display = "Detected"

            # 2. Perform Translation
            translated_text = translate_text(source_text, source_lang, target_lang)
            
            if translated_text:
                # Update stats
                st.session_state.character_count += len(source_text)
                
                # Update history
                history_item = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'source_text': source_text,
                    'source_lang': source_lang_display,
                    'target_lang': target_lang_name,
                    'translated_text': translated_text
                }
                st.session_state.translation_history.append(history_item)
                
                st.success("✅ Translation completed!")
                
                st.markdown("---")
                st.markdown("### 📤 Translation Result")
                
                r_col1, r_col2 = st.columns(2)
                with r_col1:
                    st.markdown(f"**Source ({source_lang_display}):**")
                    st.info(source_text)
                with r_col2:
                    st.markdown(f"**Target ({target_lang_name}):**")
                    st.success(translated_text)
            else:
                st.error("Translation returned empty result.")
    else:
        st.warning("⚠️ Please enter text first.")

# ============================================================================
# SECTION 13: HISTORY
# ============================================================================

st.markdown("---")
st.markdown("### 📜 Translation History")

if st.session_state.translation_history:
    for idx, item in enumerate(reversed(st.session_state.translation_history[-10:]), 1):
        with st.expander(f"#{idx} - {item['timestamp']}"):
            st.text(f"From: {item['source_text'][:50]}...")
            st.text(f"To: {item['translated_text'][:50]}...")
    
    if st.button("🗑️ Clear History"):
        st.session_state.translation_history = []
        st.rerun()
else:
    st.info("No translations yet.")

