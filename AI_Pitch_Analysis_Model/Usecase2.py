# Import Streamlit for creating the web app interface
import streamlit as st
# Import pdfplumber for extracting text from PDF files
import pdfplumber
# Import requests for fetching PDFs from URLs
import requests
# Import Google Gemini AI for pitch deck analysis
import google.generativeai as genai
# Import json for handling JSON data from API responses
import json
# Import BytesIO for handling binary data like PDFs in memory
from io import BytesIO
# Import pytesseract for OCR text extraction from images
import pytesseract
# Import PIL's Image module for image processing in OCR
from PIL import Image
# Import re for regular expression text preprocessing
import re
# Import os for file system operations
import os

# 🔹 Configure Gemini API
genai.configure(api_key="AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0")
GEMINI_MODEL = "models/gemini-1.5-flash-001-tuning"

# 🔹 Section Weights & Criteria
DEFAULT_WEIGHTS = {
    "Problem": 0.15, "Solution": 0.20, "Market": 0.20,
    "Business Model": 0.10, "Financials": 0.10, "Team": 0.25
}
if 'WEIGHTS' not in st.session_state:
    st.session_state['WEIGHTS'] = DEFAULT_WEIGHTS.copy()
if 'temp_weights' not in st.session_state:
    st.session_state['temp_weights'] = st.session_state['WEIGHTS'].copy()
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state['uploaded_file_name'] = None
SECTIONS = list(DEFAULT_WEIGHTS.keys())
CRITERIA = {
    "Problem": "Clarity of the issue, significance, urgency of need",
    "Solution": "Clarity, effectiveness, uniqueness, feasibility",
    "Market": "Market size, growth potential, target audience definition, competitive landscape",
    "Business Model": "Revenue streams, pricing clarity, scalability, sales strategy",
    "Financials": "Realism of projections, funding needs, use of funds, financial clarity",
    "Team": "Relevant experience, skills, track record, team cohesion"
}

# 🔹 Enhanced Aesthetic CSS
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 15px; }
    .subtitle { font-size: 18px; color: #78909C; text-align: center; margin-bottom: 25px; }
    .card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05); margin-bottom: 15px; border-left: 5px solid #1E88E5; }
    .score { font-weight: bold; color: #2ECC71; font-size: 18px; }
    .feedback { color: #37474F; line-height: 1.6; }
    .stProgress > div > div > div > div { background-color: #1E88E5; }
    .sidebar .sidebar-content { background-color: #F5F7FA; padding: 20px; border-radius: 10px; }
    .stButton>button { background-color: #1E88E5; color: white; border-radius: 8px; padding: 10px 20px; }
    .stButton>button:hover { background-color: #1565C0; }
    </style>
""", unsafe_allow_html=True)

# 🔹 Text Extraction Functions
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text.strip())
    text = re.sub(r'[^\w\s.,-]', '', text)
    text = re.sub(r'Page \d+', '', text)
    text = re.sub(r'^\d+\s+', '', text, flags=re.MULTILINE)
    return text

def extract_pdf_text(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        if not text.strip():
            st.warning("📄 No text extracted via parsing. Trying OCR...")
            text = ""
            for page in pdfplumber.open(pdf_file).pages:
                img = page.to_image(resolution=300).original
                text += pytesseract.image_to_string(img) + " "
            text = text.strip()
        return preprocess_text(text) if text else None
    except Exception as e:
        st.error(f"❌ Text extraction failed: {e}")
        return None

def fetch_pdf_from_url(url):
    if "drive.google.com/file/d/" in url and "/view" in url:
        file_id = url.split("/d/")[1].split("/")[0]
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
    elif "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()
        pdf_file = BytesIO(response.content)
        text = extract_pdf_text(pdf_file)
        return text
    except requests.RequestException as e:
        st.error(f"❌ Failed to fetch PDF: {e}")
        return None

def extract_text_from_uploaded_file(uploaded_file):
    pdf_file = BytesIO(uploaded_file.read())
    return extract_pdf_text(pdf_file)

# 🔹 Section Extraction and Evaluation
def extract_sections_gemini(text):
    prompt = (
        f"Extract text for these sections from the pitch deck: {', '.join(SECTIONS)}.\n"
        "Return a valid JSON object in this format:\n"
        "```json\n"
        "{\n" + "\n".join([f'  "{section}": "<Extracted text or Missing>"' for section in SECTIONS]) + "\n"
        "}\n"
        "```\n"
        "Pitch Deck Content:\n" + text
    )
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        json_match = re.search(r'```json\n(.*?)\n```', response.text.strip(), re.DOTALL)
        return json.loads(json_match.group(1)) if json_match else {section: "Missing" for section in SECTIONS}
    except Exception as e:
        st.error(f"❌ Section extraction failed: {e}")
        return {section: "Missing" for section in SECTIONS}

def evaluate_section_gemini(section_name, section_text):
    if section_text == "Missing":
        return 0, "This section is missing. Consider adding it to strengthen your pitch."
    
    prompt = (
        f"Evaluate the '{section_name}' section based on: {CRITERIA[section_name]}.\n"
        "Return a valid JSON object in this format:\n"
        "```json\n"
        "{\n"
        '  "score": <integer between 0-10>,\n'
        '  "strengths": "<Key strengths>",\n'
        '  "weaknesses": "<Areas needing improvement>",\n'
        '  "suggestions": "<Content improvements or additional data needed>"\n'
        "}\n"
        "```\n"
        "Section Content:\n" + section_text
    )
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        json_match = re.search(r'```json\n(.*?)\n```', response.text.strip(), re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
            feedback = f"**Strengths**: {result.get('strengths', 'N/A')}\n**Weaknesses**: {result.get('weaknesses', 'N/A')}\n**Suggestions**: {result.get('suggestions', 'N/A')}"
            return result.get("score", 0), feedback
        return 0, "Evaluation failed: Invalid response format."
    except Exception as e:
        st.error(f"❌ Evaluation failed for {section_name}: {e}")
        return 0, "Evaluation failed due to API error."

def analyze_pitch_deck(text):
    if not text:
        return None, None, None
    section_texts = extract_sections_gemini(text)
    section_scores, feedbacks = {}, {}
    for section in SECTIONS:
        score, feedback = evaluate_section_gemini(section, section_texts.get(section, "Missing"))
        section_scores[section] = score
        feedbacks[section] = feedback
    total_score = sum(section_scores[section] / 10 * st.session_state['WEIGHTS'][section] for section in SECTIONS) * 100
    return total_score, section_scores, feedbacks

# 🔹 Sidebar Functionality
with st.sidebar:
    st.markdown("### ⚙️ Analysis Settings")
    st.write("Customize your pitch deck analysis:")
    
    for section in SECTIONS:
        st.session_state['temp_weights'][section] = st.slider(f"{section} Weight", 0.0, 1.0, st.session_state['temp_weights'][section], 0.05, key=f"slider_{section}")
    
    if st.button("Update Weights", use_container_width=True):
        with st.spinner("Updating weights..."):
            st.session_state['WEIGHTS'] = st.session_state['temp_weights'].copy()
            st.success("Weights successfully updated")
    
    if st.button("Reset Weights", use_container_width=True):
        st.session_state['temp_weights'] = DEFAULT_WEIGHTS.copy()
        st.session_state['WEIGHTS'] = DEFAULT_WEIGHTS.copy()
        st.success("Weights reset to default")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write("AI-powered pitch deck analysis using Google Gemini. Adjust weights to prioritize sections based on your needs.")

# 🔹 Main UI
st.markdown('<div class="main-title">AI Pitch Deck Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Unlock Insights for Your Startup Pitch with AI</div>', unsafe_allow_html=True)

with st.container():
    input_method = st.radio("Choose Input Method", ("📤 Upload PDF", "🔗 Enter URL"), horizontal=True, key="input_method")

    if input_method == "📤 Upload PDF":
        uploaded_file = st.file_uploader("Upload your pitch deck PDF", type=["pdf"], label_visibility="collapsed")
        if uploaded_file and st.button("Analyze PDF", use_container_width=True):
            st.session_state['uploaded_file_name'] = uploaded_file.name.rsplit('.', 1)[0]  # Store file name without extension
            with st.spinner("Analyzing your pitch deck..."):
                text = extract_text_from_uploaded_file(uploaded_file)
                total_score, section_scores, feedbacks = analyze_pitch_deck(text)
                if total_score is not None:
                    st.session_state['analysis_results'] = {
                        'total_score': total_score,
                        'section_scores': section_scores,
                        'feedbacks': feedbacks
                    }
                else:
                    st.session_state['analysis_results'] = None
                    st.error("❌ Analysis failed. Please check your file.")
    else:
        url = st.text_input("Enter Pitch Deck URL", placeholder="e.g., https://drive.google.com/...")
        if st.button("Analyze URL", use_container_width=True):
            st.session_state['uploaded_file_name'] = None  # Reset file name for URL input
            with st.spinner("Fetching and analyzing your pitch deck..."):
                text = fetch_pdf_from_url(url)
                total_score, section_scores, feedbacks = analyze_pitch_deck(text)
                if total_score is not None:
                    st.session_state['analysis_results'] = {
                        'total_score': total_score,
                        'section_scores': section_scores,
                        'feedbacks': feedbacks
                    }
                else:
                    st.session_state['analysis_results'] = None
                    st.error("❌ Analysis failed. Please check the URL.")

if st.session_state['analysis_results']:
    results = st.session_state['analysis_results']
    st.success(f"🎉 Pitch Score: **{results['total_score']:.2f}/100 **")
    st.progress(int(results['total_score']))
    st.markdown("### Detailed Feedback")
    for section in SECTIONS:
        with st.expander(f"📑 {section}", expanded=False):
            st.markdown(f"""
                <div class="card">
                    <span class="score">Score: {results['section_scores'][section]}/10</span><br>
                    <span class="feedback">{results['feedbacks'][section]}</span>
                </div>
            """, unsafe_allow_html=True)
    
    # Generate the analysis content
    download_content = f"Pitch Deck Analysis Results\n\n"
    download_content += f"Total Pitch Score: {results['total_score']:.2f}/100\n\n"
    download_content += "Detailed Feedback:\n"
    for section in SECTIONS:
        download_content += f"\n{section}:\n"
        download_content += f"Score: {results['section_scores'][section]}/10\n"
        download_content += f"{results['feedbacks'][section]}\n"
        download_content += "-" * 50 + "\n"
    
    # Determine the file name based on input method
    base_file_name = st.session_state['uploaded_file_name'] if st.session_state['uploaded_file_name'] else "pitch_deck_analysis"
    download_file_name = f"{base_file_name}_results.txt"
    
    # Save the file locally in the same directory as the script
    output_path = os.path.join(os.getcwd(), download_file_name)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(download_content)
        st.success(f"Results saved to: `{output_path}`")
    except Exception as e:
        st.error(f"Failed to save file locally: {e}")
    
    # Provide download button as a fallback
    st.download_button(
        label="Download Results",
        data=download_content,
        file_name=download_file_name,
        mime="text/plain",
        use_container_width=True
    )

st.markdown("---")
st.markdown('<div style="text-align: center; color: #78909C;">Powered by Google Gemini • Built with Streamlit</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #78909C;">Developed By Amresh Yadav • Email Id: maithilgeek@gmail.com, Mob. - 7260905948</div>', unsafe_allow_html=True)