import streamlit as st
import google.generativeai as genai
from PIL import Image
import pytesseract
import pandas as pd

# 🔹 Set the correct path to the installed tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract.exe"

# 🔹 Configure Gemini API
genai.configure(api_key="AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0")  # Default API key
AVAILABLE_MODELS = [
    "gemini-1.5-flash-001-tuning",
    "gemini-1.5-pro",
    "gemini-1.0-pro"
]

# 🔹 Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    body { 
        font-family: 'Roboto', sans-serif; 
        background-color: #F5F6F5; 
        color: #202124; 
    }
    .main-title { 
        font-size: 34px; 
        font-weight: 700; 
        color: #1A73E8; 
        text-align: center; 
        margin-top: 25px; 
        margin-bottom: 10px; 
    }
    .subtitle { 
        font-size: 16px; 
        color: #5F6368; 
        text-align: center; 
        margin-bottom: 30px; 
    }
    .chat-box { 
        background-color: #FFFFFF; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); 
        margin-bottom: 20px; 
        border: 1px solid #E8ECEF; 
    }
    .user-msg { 
        background-color: #E3F2FD; 
        padding: 10px; 
        border-radius: 8px; 
        margin-bottom: 10px; 
    }
    .bot-msg { 
        background-color: #F1F8E9; 
        padding: 10px; 
        border-radius: 8px; 
        margin-bottom: 10px; 
    }
    .stButton>button { 
        background-color: #1A73E8; 
        color: white; 
        border-radius: 10px; 
        padding: 10px 20px; 
        font-weight: 500; 
        border: none; 
    }
    .stButton>button:hover { 
        background-color: #1557B0; 
    }
    .footer { 
        text-align: center; 
        color: #5F6368; 
        font-size: 12px; 
        margin-top: 40px; 
    }
    </style>
""", unsafe_allow_html=True)

# 🔹 Chat Function with Context
def get_gemini_response(query, model, chat_history):
    try:
        gen_model = genai.GenerativeModel(model)
        # Build context from chat history
        context = "Previous conversation:\n"
        for msg in chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['text']}\n"
        full_prompt = f"{context}\nUser: {query}"
        response = gen_model.generate_content(full_prompt)
        if hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            return "Sorry, I couldn’t generate a response. Try again!"
    except Exception as e:
        return f"Error: {str(e)}"

# 🔹 Function to Calculate OCR Confidence
def get_ocr_confidence(image):
    try:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DATAFRAME)
        valid_data = data[(data['text'].notna()) & (data['text'].str.strip() != '') & (data['conf'] > 0)]
        if not valid_data.empty:
            average_confidence = valid_data['conf'].mean()
            return average_confidence
        else:
            return 0.0
    except Exception as e:
        return f"Error calculating confidence: {str(e)}"

# 🔹 UI Layout
st.markdown('<div class="main-title">🤖 Chat Assistant with Image Extractor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Chat with me or use extracted text from images 🌟</div>', unsafe_allow_html=True)

# 🔹 Sidebar for Model Selection and Image Text Extractor
with st.sidebar:
    st.markdown("### Settings ⚙️")
    
    gemini_api_key = st.text_input(
        "Enter your Gemini API Key 🔐",
        type="password",
        placeholder="Enter your Gemini API Key...",
        help="Your Gemini API key is used securely and not shared."
    )

    if not gemini_api_key:
        gemini_api_key = "AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0"
    
    genai.configure(api_key=gemini_api_key)

    selected_model = st.selectbox(
        "Select AI Model 🤖",
        AVAILABLE_MODELS,
        index=0,
        help="Choose the Gemini model for chatting."
    )

    st.markdown("---")
    st.markdown("### 🖼️ Image Text Extractor")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        extracted_text = pytesseract.image_to_string(img)
        st.subheader("Extracted Text")
        st.text_area("Text", extracted_text, height=200, key="extracted_text")

        with st.spinner("Calculating OCR confidence..."):
            confidence = get_ocr_confidence(img)
        if isinstance(confidence, float):
            st.markdown(f"**OCR Confidence:** {confidence:.2f}%")
            if confidence < 50:
                st.warning("Low confidence detected. The extracted text may be inaccurate.")
        else:
            st.error(confidence)

    st.markdown("---")
    st.write(f"Powered by Google Gemini ({selected_model}) ✨")

# 🔹 Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔹 Chat Input with Unique Key
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

user_input = st.text_input("Type your message or use extracted text...", key=f"user_input_{st.session_state.input_key}")

# 🔹 Submit Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Send 🚀"):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            with st.spinner("Thinking..."):
                response = get_gemini_response(user_input, selected_model, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "bot", "text": response})
            # Clear input by incrementing key
            st.session_state.input_key += 1
            st.rerun()

with col2:
    if st.button("Send Extracted Text 📸") and "extracted_text" in st.session_state:
        extracted_text = st.session_state.get("extracted_text", "")
        if extracted_text:
            st.session_state.chat_history.append({"role": "user", "text": f"Query based on extracted text: {extracted_text}"})
            with st.spinner("Processing extracted text..."):
                response = get_gemini_response(f"Provide information based on this extracted text: {extracted_text}", selected_model, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "bot", "text": response})
            # Clear input by incrementing key
            st.session_state.input_key += 1
            st.rerun()

# 🔹 Display Chat History
if st.session_state.chat_history:
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg"><b>You:</b> {msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg"><b>Bot:</b> {msg["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<div class="footer">Built with Streamlit • Powered by Google Gemini<br>Developed by Amresh Yadav • maithilgeek@gmail.com</div>', unsafe_allow_html=True)