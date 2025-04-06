import streamlit as st
import google.generativeai as genai
import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 🔹 Configure Gemini API (API key will be set dynamically later)
genai.configure(api_key="AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0")  # Default API key

# 🔹 Available Models
AVAILABLE_MODELS = [
    "gemini-1.5-flash-001-tuning",
    "gemini-1.5-pro",
    "gemini-1.0-pro"
]

# 🔹 Custom Styling (Single Light Theme)
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
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); 
    }
    .subtitle { 
        font-size: 16px; 
        color: #5F6368; 
        text-align: center; 
        margin-bottom: 30px; 
    }
    .card { 
        background-color: #FFFFFF; 
        padding: 30px; 
        border-radius: 15px; 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); 
        margin-bottom: 25px; 
        border: 2px solid #E8ECEF; 
        transition: transform 0.2s ease, box-shadow 0.2s ease; 
    }
    .card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15); 
    }
    .stButton>button { 
        background-color: #1A73E8; 
        color: white; 
        border-radius: 10px; 
        padding: 12px 28px; 
        font-weight: 500; 
        border: none; 
        transition: background-color 0.2s ease, transform 0.2s ease; 
    }
    .stButton>button:hover { 
        background-color: #1557B0; 
        transform: scale(1.05); 
    }
    .section-header { 
        font-size: 22px; 
        font-weight: 500; 
        color: #1A73E8; 
        margin-bottom: 20px; 
    }
    .footer { 
        text-align: center; 
        color: #5F6368; 
        font-size: 12px; 
        margin-top: 40px; 
    }
    .json-section { 
        font-size: 16px; 
        color: #202124; 
        margin-bottom: 12px; 
        font-weight: 500; 
    }
    .json-content { 
        font-size: 14px; 
        color: #4B5563; 
        margin-left: 20px; 
    }
    </style>
""", unsafe_allow_html=True)

# 🔹 Gemini PhD Research Guide Generation
def generate_research_guide(scholar_details, selected_model):
    prompt = f"""You are an expert academic advisor with extensive knowledge in research trends across disciplines. I am a PhD scholar seeking guidance on the top five best areas to research based on my profile. Please analyze my details carefully and provide a personalized list of research areas that align with my background, interests, and goals.

    Here are my details:
    {scholar_details}

    Provide a structured response in JSON format with the following schema:
    {{
        "research_areas": [
            {{"area": "string", "description": "string"}},
            {{"area": "string", "description": "string"}},
            {{"area": "string", "description": "string"}},
            {{"area": "string", "description": "string"}},
            {{"area": "string", "description": "string"}}
        ]
    }}
    Ensure the response includes exactly five research areas with concise, relevant descriptions tailored to my input. Return only the JSON string, no additional text or markdown.
    """
    try:
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(prompt)
        if hasattr(response, 'text') and response.text:
            return json.loads(response.text.strip())
        else:
            return {"error": "No valid response from Gemini API."}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from Gemini API."}
    except Exception as e:
        return {"error": f"Error generating guide with {selected_model}: {str(e)}"}

# 🔹 Function to Generate PDF
def generate_pdf(guide, name):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    styles['Title'].fontSize = 18
    styles['Title'].textColor = '#1A73E8'
    styles['Heading2'].fontSize = 14
    styles['Heading2'].textColor = '#1A73E8'
    styles['Normal'].fontSize = 12

    story.append(Paragraph(f"📚 PhD Research Guide for {name}", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("🔍 Top 5 Research Areas", styles['Heading2']))
    for i, area in enumerate(guide["research_areas"], 1):
        story.append(Paragraph(f"{i}. {area['area']}", styles['Normal']))
        story.append(Paragraph(f"Description: {area['description']}", styles['Normal']))
        story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer

# 🔹 UI Layout
st.markdown('<div class="main-title">📚 PhD Scholar Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find your top research areas with AI-powered insights 🌟</div>', unsafe_allow_html=True)

# 🔹 Sidebar with Model Toggle
with st.sidebar:
    st.markdown("### Home 🖥️")
    
    gemini_api_key = st.text_input(
        "Enter your Gemini API Key 🔐",
        type="password",
        placeholder="Enter your Gemini API Key...",
        help="Your Gemini API key is used securely and not shared."
    )

    if not gemini_api_key:
        gemini_api_key = "AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0"
    
    # Reconfigure API key dynamically
    genai.configure(api_key=gemini_api_key)

    selected_model = st.selectbox(
        "Select AI Model 🤖",
        AVAILABLE_MODELS,
        index=0,
        help="Choose the Gemini model to generate your research guide."
    )

    st.write("Fill out the form to get your personalized research guide!. Note: Select gemini-1.5-flash-001-tuning if you don't have api key for gemini-1.5-pro or gemini-1.0-pro.")
    st.markdown("---")
    st.write(f"Powered by Google Gemini ({selected_model}) ✨")

# 🔹 Form for Scholar Details
with st.form("scholar_form"):
    st.markdown('<div class="section-header">🎓 Your Academic Profile</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", value="", key="name")
        degree = st.text_input("Current Degree (e.g., MSc, BTech)", value="", key="degree")
        field = st.text_input("Field of Study (e.g., Computer Science, Biology)", value="", key="field")
    with col2:
        interests = st.text_area("Research Interests", value="None", height=100, key="interests")
        experience = st.text_area("Relevant Experience (e.g., projects, publications)", value="None", height=100, key="experience")
        goals = st.text_area("Research Goals (e.g., industry impact, academic contribution)", value="None", height=100, key="goals")

    submitted = st.form_submit_button("Generate Research Guide 🎉")

if submitted:
    if not name:
        st.error("Please enter your name! 📝")
    elif not field:
        st.error("Please enter your field of study! 📚")
    else:
        scholar_profile = f"""
        Name: {name}
        Current Degree: {degree}
        Field of Study: {field}
        Research Interests: {interests}
        Relevant Experience: {experience}
        Research Goals: {goals}
        """

        st.markdown("---")
        st.subheader(f"📚 Research Guide for {name}")

        with st.spinner(f"Analyzing your profile with {selected_model}... 🌟"):
            guide = generate_research_guide(scholar_profile, selected_model)

        if isinstance(guide, dict) and "error" in guide:
            st.markdown(f"<div class='card'><b>Oops! 😢</b> {guide['error']}</div>", unsafe_allow_html=True)
        else:
            with st.expander("View Your Research Areas 🌈", expanded=True):
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<b class='json-section'>🔍 Top 5 Research Areas</b>", unsafe_allow_html=True)
                for i, area in enumerate(guide["research_areas"], 1):
                    st.markdown(f"<div class='json-content'>{i}. <b>{area['area']}</b></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Description: {area['description']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            pdf_buffer = generate_pdf(guide, name)
            st.download_button(
                label="Download Guide (PDF) 📑",
                data=pdf_buffer,
                file_name=f"{name}_research_guide.pdf",
                mime="application/pdf"
            )

# Footer
st.markdown("---")
st.markdown('<div class="footer">Powered by Google Gemini • Built with Streamlit<br>Developed by Amresh Yadav • maithilgeek@gmail.com</div>', unsafe_allow_html=True)