# ============================================================================
# APP: AI-Powered Language Translator & Text-to-Speech
# AUTHOR: CodeAlpha (Refactored for Professional Deployment)
# DESCRIPTION: A Streamlit web application utilizing Deep Translator for
#              text translation and gTTS for audio synthesis.
# ============================================================================

import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from datetime import datetime
from gtts import gTTS
from io import BytesIO

# ============================================================================
# SECTION 1: CONFIGURATION & ASSETS
# ============================================================================

st.set_page_config(
    page_title="AI Neural Translator",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS for a modern, flat design aesthetic
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header Styling */
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Input/Output Area Styling */
    .stTextArea textarea {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        font-size: 16px;
    }
    
    /* Action Button Styling */
    .stButton button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Audio Player Width Fix */
    .stAudio {
        width: 100%;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SECTION 2: SESSION STATE MANAGEMENT
# ============================================================================

# Initialize session state for persistence across re-runs
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

# ============================================================================
# SECTION 3: UTILITY FUNCTIONS & CONSTANTS
# ============================================================================

# Supported Languages Mapping (ISO 639-1 Codes)
LANGUAGES = {
    'ar': 'Arabic', 'en': 'English', 'fr': 'French', 'de': 'German', 
    'es': 'Spanish', 'it': 'Italian', 'ja': 'Japanese', 'ru': 'Russian',
    'tr': 'Turkish', 'zh-CN': 'Chinese (Simplified)', 'hi': 'Hindi', 'ko': 'Korean'
}

def text_to_speech(text: str, lang_code: str) -> BytesIO:
    """
    Generates audio from text using Google Text-to-Speech (gTTS).
    
    Args:
        text (str): The translated text to convert to speech.
        lang_code (str): The ISO 639-1 language code (e.g., 'en', 'ar').
        
    Returns:
        BytesIO: An in-memory binary stream containing the MP3 audio data.
                 Returns None if generation fails.
    """
    try:
        # Sanitize language code (gTTS usually expects 2-letter codes, exception for Chinese)
        target_lang = lang_code
        if len(lang_code) > 2 and lang_code != 'zh-CN':
            target_lang = lang_code[:2]
            
        # Generate speech
        tts = gTTS(text=text, lang=target_lang, slow=False)
        
        # Write to in-memory buffer to avoid file system I/O operations
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0) # Reset pointer to the beginning of the file
        
        return audio_buffer
        
    except Exception as e:
        # Log error to console (or handle gracefully in UI)
        print(f"TTS Error: {e}")
        return None

# ============================================================================
# SECTION 4: SIDEBAR INTERFACE
# ============================================================================

with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("---")
    
    st.info(
        """
        **System Status:**
        - Translation Engine: **Active**
        - Audio Synthesis: **Active**
        - Environment: **Production**
        """
    )
    
    st.markdown("### History Management")
    if st.button("🗑️ Clear Session History", use_container_width=True):
        st.session_state.translation_history = []
        st.rerun()

    st.markdown("---")
    st.caption("v2.0.1 | Engineered with Streamlit")

# ============================================================================
# SECTION 5: MAIN APPLICATION LOGIC
# ============================================================================

# Header
st.title("🌍 Neural Language Translator")
st.markdown("### Instant Translation with Synthesis Support")
st.markdown("---")

# Layout: Split screen for Input and Output
col_input, col_output = st.columns(2, gap="medium")

# --- LEFT COLUMN: SOURCE INPUT ---
with col_input:
    st.subheader("📝 Source Input")
    
    # Language Selection
    source_lang_label = st.selectbox(
        "Source Language",
        ["Auto-detect"] + list(LANGUAGES.values()),
        key="src_lang_select"
    )
    
    # Text Input Area
    source_text = st.text_area(
        "Enter text to translate:",
        height=250,
        placeholder="Type or paste content here...",
        help="Supports automatic language detection."
    )

# --- RIGHT COLUMN: TRANSLATION OUTPUT ---
with col_output:
    st.subheader("🎯 Target Output")
    
    # Target Language Selection (Default to Arabic for convenience)
    target_lang_label = st.selectbox(
        "Target Language",
        list(LANGUAGES.values()),
        index=0, # Index 0 is Arabic in our dict
        key="tgt_lang_select"
    )
    
    # Resolve Language Codes
    if source_lang_label == "Auto-detect":
        source_code = 'auto'
    else:
        # Reverse lookup to find key by value
        source_code = [k for k, v in LANGUAGES.items() if v == source_lang_label][0]
        
    target_code = [k for k, v in LANGUAGES.items() if v == target_lang_label][0]

    # Placeholder container for results to ensure layout stability
    result_container = st.empty()

# --- ACTION SECTION ---
st.markdown("---")
col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 2, 1])

with col_btn_2:
    process_btn = st.button("🚀 Process Translation & Generate Audio", use_container_width=True)

# --- EXECUTION LOGIC ---
if process_btn:
    if not source_text.strip():
        st.warning("⚠️ Input buffer is empty. Please enter text to proceed.")
    else:
        with st.spinner("🔄 Processing request... Please wait."):
            try:
                # Step 1: Perform Translation
                translator = GoogleTranslator(source=source_code, target=target_code)
                translated_text = translator.translate(source_text)
                
                # Step 2: Generate Audio
                audio_data = text_to_speech(translated_text, target_code)
                
                # Step 3: Render Results
                with col_output:
                    st.success(translated_text)
                    if audio_data:
                        st.markdown("**🔊 Audio Playback:**")
                        st.audio(audio_data, format='audio/mp3')
                
                # Step 4: Update History (Append to Session State)
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.translation_history.append({
                    "time": timestamp,
                    "src_txt": source_text,
                    "tgt_txt": translated_text,
                    "lang_pair": f"{source_lang_label} → {target_lang_label}"
                })
                
            except Exception as e:
                st.error(f"❌ System Error: {str(e)}")

# ============================================================================
# SECTION 6: HISTORICAL DATA VIEW
# ============================================================================

if st.session_state.translation_history:
    st.markdown("---")
    st.subheader("📜 Recent Activity Log")
    
    # Display last 5 records in reverse chronological order
    for record in reversed(st.session_state.translation_history[-5:]):
        with st.expander(f"[{record['time']}] {record['lang_pair']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.caption("Original:")
                st.write(record['src_txt'])
            with col_b:
                st.caption("Translated:")
                st.write(record['tgt_txt'])
