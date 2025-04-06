
# 📚 PhD Scholar Assistant

An AI-powered assistant to help PhD scholars discover the top 5 personalized research areas based on their academic profile. Built with **Streamlit** and powered by **Google Gemini models**.

## 🚀 Features

- 🤖 Uses Gemini models (`gemini-1.5-flash-001-tuning`, `gemini-1.5-pro`, and `gemini-1.0-pro`) for intelligent research guidance.
- 🎓 Collects academic details like degree, field, research interests, and goals.
- 📑 Generates a JSON response with 5 recommended research areas and their descriptions.
- 📄 Converts results into a downloadable PDF report using `reportlab`.
- ✨ Clean, aesthetic, and interactive user interface.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [Google Generative AI (Gemini)](https://ai.google.dev/)
- **PDF Generator**: `reportlab`
- **Styling**: Custom CSS for a modern and clean UI

## 🔑 API Key

You can enter your **Google Gemini API Key** via the sidebar. If no key is entered, the app uses a default fallback key (demo/testing only).

> ⚠️ **Note**: For production usage, it's highly recommended to use your own secure API key.

## 💡 How it Works

1. Fill in your academic details in the form.
2. Select a Gemini model from the sidebar.
3. Click "Generate Research Guide".
4. View results on the screen or download as PDF.

## 📦 Installation

```bash
pip install streamlit google-generativeai reportlab
```

## ▶️ Run the App

```bash
streamlit run assistant.py
```

## 🧑‍💻 Developer

**Amresh Yadav**  
✉️ maithilgeek@gmail.com

---

