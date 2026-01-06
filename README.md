# 🔮 AI Neural Translator Pro

![Project Screenshot](Demo/screenshot.png)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 📄 Project Overview
**AI Neural Translator Pro** is a comprehensive, real-time language translation dashboard built with Python and Streamlit. It leverages the **Google Translate API** (via `deep-translator`) for high-accuracy translation across 100+ languages and integrates **Google Text-to-Speech (gTTS)** for audio synthesis.

This project demonstrates the integration of NLP tools into a modern, user-friendly web interface with advanced features like text analytics and session history tracking.

---

## ✨ Key Features

* **⚡ Instant Translation:** Real-time translation supporting over 100 languages using synchronous API calls.
* **🔊 Text-to-Speech (TTS):** Integrated audio synthesis engine to pronounce translated text with native accents.
* **📊 Smart Text Analytics:** Automatic calculation of character and word counts for the source text.
* **🎨 Modern UI:** A "Glassmorphism" inspired design with a clean, responsive layout using custom CSS.
* **📜 History Logging:** Session-based tracking of previous translations for quick reference.
* **🤖 Auto-Detection:** Intelligent source language detection using `langdetect`.

---

## 🛠️ Technology Stack

* **Framework:** [Streamlit](https://wkvuyma46wjw5r5dbss4wr.streamlit.app/) (Web App Interface)
* **Translation Engine:** [Deep Translator](https://github.com/nidhaloff/deep-translator)
* **Audio Synthesis:** [gTTS](https://github.com/pndurette/gTTS) (Google Text-to-Speech)
* **Language Detection:** `langdetect` library
* **Data Handling:** Python `io` (BytesIO for in-memory audio processing) & Session State

---

## 📂 Repository Structure

Here is an overview of the files included in this repository:

| File Name | Description |
| :--- | :--- |
| `app.py` | The main application source code containing the Streamlit logic, UI layout, and helper functions. |
| `Demo/` | **Contains project screenshots and a video demonstration of the app in action.** |
| `requirements.txt` | List of all Python dependencies required to run the project (streamlit, gTTS, etc.). |
| `README.md` | Project documentation and setup guide. |
| `LICENSE` | The license agreement (MIT) governing the use and distribution of this software. |

---

## 🎥 Demo & Usage

**Check the `Demo/` folder for a complete video walkthrough.**

### How to use:
1.  **Enter Text:** Type or paste text into the source input area.
2.  **Select Language:** Choose the target language from the dropdown menu.
3.  **Analyze:** View real-time word and character counts.
4.  **Translate:** Click the **"🚀 Translate & Analyze"** button.
5.  **Listen:** Use the audio player to hear the pronunciation of the translated text.

---

## 🚀 Installation & Setup

Follow these steps to run the application locally:

**1. Clone the repository:**
```bash
git clone (https://github.com/eslamalsaeed72-droid/CodeAlpha_-Language-Translation-Tool-.git)
cd RepoName

```

**2. Install dependencies:**
It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt

```

**3. Run the application:**

```bash
streamlit run app.py

```

The app will launch automatically in your default web browser at `http://localhost:8501`.

---

## 👤 Author

**Eslam** *Mechatronics Engineer | AI & Embedded Systems Enthusiast*

---


بهذا الشكل، أول ما ترفع الملفات على GitHub، الصورة ستظهر تلقائياً في واجهة المشروع، وسيكون كل شيء منظماً باحترافية.

```
