import streamlit as st
import google.generativeai as genai
import json
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 🔹 Configure Gemini API
genai.configure(api_key="AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0")  # Replace with your valid API key
GEMINI_MODEL = "gemini-1.5-flash-001-tuning"  # Corrected model name format

# 🔹 Custom Styling (Baby-Themed)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    body { 
        font-family: 'Roboto', sans-serif; 
        background-color: #E6F0FA; 
        color: #202124; 
    }
    .main-title { 
        font-size: 34px; 
        font-weight: 700; 
        color: #4285F4; 
        text-align: center; 
        margin-top: 25px; 
        margin-bottom: 10px; 
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); 
    }
    .subtitle { 
        font-size: 16px; 
        color: #6B7280; 
        text-align: center; 
        margin-bottom: 30px; 
    }
    .card { 
        background-color: #FFFFFF; 
        padding: 30px; 
        border-radius: 15px; 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); 
        margin-bottom: 25px; 
        border: 2px solid #D1E5F4; 
        transition: transform 0.2s ease, box-shadow 0.2s ease; 
    }
    .card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15); 
    }
    .stButton>button { 
        background-color: #34C759; 
        color: white; 
        border-radius: 10px; 
        padding: 12px 28px; 
        font-weight: 500; 
        border: none; 
        transition: background-color 0.2s ease, transform 0.2s ease; 
    }
    .stButton>button:hover { 
        background-color: #2DA44E; 
        transform: scale(1.05); 
    }
    .section-header { 
        font-size: 22px; 
        font-weight: 500; 
        color: #4285F4; 
        margin-bottom: 20px; 
    }
    .footer { 
        text-align: center; 
        color: #6B7280; 
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

# 🔹 Gemini Baby Guide Generation
def generate_baby_guide(baby_details, age_unit="months"):
    prompt = f""" You are a baby care expert and a best baby doctor. I need your help to create a personalized baby care guide for my baby. Please analyze the given details carefully check age and weight of baby and suggest parents best to do for an ideal and healthy baby.
    I am a new parent and I need the best personalized guidance based on the following information please mention if we need to visit Doctor or not:
    {baby_details}

    Provide a structured baby care guide in JSON format with the following schema:
    {{
        "feeding": {{"timing": "string", "quantity": "string", "foods": "string"}},
        "sleeping_routines": {{"total_hours": "string", "routine": "string"}},
        "milestone_tracking": {{"age_specific_milestones": "string"}},
        "daily_schedule": {{"schedule": "string"}},
        "health_concerns": {{"concerns": "string", "tips": "string"}},
        "emotional_bonding": {{"bonding": "string", "development": "string"}},
        "parenting_tips": {{"tips": "string"}}
    }}
    Ensure all fields are filled with relevant, concise information based on the input, tailored for a baby whose age is in {age_unit}.
    Return only the JSON string, no additional text or markdown.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        if hasattr(response, 'text') and response.text:
            return json.loads(response.text.strip())
        else:
            return {"error": "No valid response from Gemini API."}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from Gemini API."}
    except Exception as e:
        return {"error": f"Error generating guide: {str(e)}"}

# 🔹 Function to Generate PDF
def generate_pdf(guide, name):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    styles['Title'].fontSize = 18
    styles['Title'].textColor = '#4285F4'
    styles['Heading2'].fontSize = 14
    styles['Heading2'].textColor = '#4285F4'
    styles['Normal'].fontSize = 12

    story.append(Paragraph(f"👶 Baby Care Guide for {name}", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("🍼 1. Feeding", styles['Heading2']))
    story.append(Paragraph(f"Timing: {guide['feeding']['timing']}", styles['Normal']))
    story.append(Paragraph(f"Quantity: {guide['feeding']['quantity']}", styles['Normal']))
    story.append(Paragraph(f"Foods: {guide['feeding']['foods']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("🌙 2. Sleeping Routines", styles['Heading2']))
    story.append(Paragraph(f"Total Hours: {guide['sleeping_routines']['total_hours']}", styles['Normal']))
    story.append(Paragraph(f"Routine: {guide['sleeping_routines']['routine']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("⭐ 3. Milestone Tracking", styles['Heading2']))
    story.append(Paragraph(f"Age-Specific Milestones: {guide['milestone_tracking']['age_specific_milestones']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("⏰ 4. Daily Schedule", styles['Heading2']))
    story.append(Paragraph(f"Schedule: {guide['daily_schedule']['schedule']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("🩺 5. Health Concerns", styles['Heading2']))
    story.append(Paragraph(f"Concerns: {guide['health_concerns']['concerns']}", styles['Normal']))
    story.append(Paragraph(f"Tips: {guide['health_concerns']['tips']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("💕 6. Emotional Bonding", styles['Heading2']))
    story.append(Paragraph(f"Bonding: {guide['emotional_bonding']['bonding']}", styles['Normal']))
    story.append(Paragraph(f"Development: {guide['emotional_bonding']['development']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("🌟 7. Parenting Tips", styles['Heading2']))
    story.append(Paragraph(f"Tips: {guide['parenting_tips']['tips']}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# 🔹 Parenting Goals Options
PARENTING_GOALS = [
    "Establish a sleep routine",
    "Introduce solid foods",
    "Encourage developmental milestones",
    "Improve feeding habits",
    "Promote emotional bonding",
    "Manage teething and health issues",
    "Create a daily schedule",
    "Reduce fussiness or crying",
    "Support language development",
    "Transition to a toddler bed",
    "Encourage independence (e.g., self-feeding)",
    "Prepare for potty training",
    "Build a consistent nap schedule",
    "Address allergies or sensitivities",
    "General care and well-being"
]

# 🔹 UI Layout with Filter
st.markdown('<div class="main-title">👶 Baby Care Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your little one’s personalized guide 🌈</div>', unsafe_allow_html=True)

# 🔹 Sidebar with Filter
# 🔹 Sidebar with Filter
with st.sidebar:
    st.markdown("### Home 🍼")
    
    # Gemini API Key Input
    gemini_api_key = st.text_input(
        "Enter your Gemini API Key 🔐",
        type="password",
        placeholder="Enter your Gemini API Key...",
        help="Your Gemini API key is used securely and not shared."
    )

    # Use default key if none is provided
    if not gemini_api_key:
        gemini_api_key = "AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0"

    
    age_filter = st.selectbox(
        "Select Age Unit 🌟",
        ["Baby Age in Months", "Baby Age in Years"],
        index=0
    )
    
    st.write("Fill out the form to get your custom guide!")
    st.markdown("---")
    st.write("Powered by Google Gemini ✨")


# 🔹 Conditional Form and Logic Based on Filter
if age_filter == "Baby Age in Months":
    with st.form("baby_form_months"):
        st.markdown('<div class="section-header">👶 Baby Details (Months)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Baby's Name", value="", key="name_months")
            age_months = st.number_input("Age (in months)", min_value=0, max_value=36, step=1, value=0, key="age_months")
            gender = st.selectbox("Gender", ["Boy", "Girl", "Prefer not to say"], index=2, key="gender_months")
            weight = st.text_input("Weight (kg)", value="", key="weight_months")
        with col2:
            allergies = st.text_area("Allergies or Sensitivities", value="None", height=100, key="allergies_months")
            health_notes = st.text_area("Medical History/Notes", value="None", height=100, key="health_notes_months")
        
        goals = st.multiselect(
            "Your Parenting Goals 🌟 (Select all that apply)",
            options=PARENTING_GOALS,
            default=["General care and well-being"],
            key="goals_months"
        )

        submitted = st.form_submit_button("Generate Guide 🎉")

    if submitted:
        if not name:
            st.error("Please enter your baby’s name! 👶")
        elif not weight:
            st.error("Please enter your baby’s weight! ⚖️")
        else:
            goals_str = ", ".join(goals) if goals else "None selected"
            baby_profile = f"""
            Name: {name}
            Age: {age_months} months
            Gender: {gender}
            Weight: {weight} kg
            Allergies: {allergies}
            Health Notes: {health_notes}
            Parenting Goals: {goals_str}
            """

            st.markdown("---")
            st.subheader(f"🍼 Care Guide for {name}")

            with st.spinner("Crafting your baby’s guide... 🌟"):
                guide = generate_baby_guide(baby_profile, "months")

            if isinstance(guide, dict) and "error" in guide:
                st.markdown(f"<div class='card'><b>Oops! 😢</b> {guide['error']}</div>", unsafe_allow_html=True)
            else:
                with st.expander("View Your Baby’s Guide 🌈", expanded=True):
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🍼 1. Feeding</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Timing: {guide['feeding']['timing']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Quantity: {guide['feeding']['quantity']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Foods: {guide['feeding']['foods']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🌙 2. Sleeping Routines</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Total Hours: {guide['sleeping_routines']['total_hours']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Routine: {guide['sleeping_routines']['routine']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>⭐ 3. Milestone Tracking</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Age-Specific Milestones: {guide['milestone_tracking']['age_specific_milestones']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>⏰ 4. Daily Schedule</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Schedule: {guide['daily_schedule']['schedule']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🩺 5. Health Concerns</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Concerns: {guide['health_concerns']['concerns']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Tips: {guide['health_concerns']['tips']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>💕 6. Emotional Bonding</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Bonding: {guide['emotional_bonding']['bonding']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Development: {guide['emotional_bonding']['development']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🌟 7. Parenting Tips</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Tips: {guide['parenting_tips']['tips']}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                pdf_buffer = generate_pdf(guide, name)
                st.download_button(
                    label="Download Guide (PDF) 📑",
                    data=pdf_buffer,
                    file_name=f"{name}_baby_care_guide.pdf",
                    mime="application/pdf"
                )

else:  # Baby Age in Years
    with st.form("baby_form_years"):
        st.markdown('<div class="section-header">👶 Baby Details (Years)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Baby's Name", value="", key="name_years")
            age_years = st.number_input("Age (in years)", min_value=0, max_value=3, step=1, value=0, key="age_years")
            gender = st.selectbox("Gender", ["Boy", "Girl", "Prefer not to say"], index=2, key="gender_years")
            weight = st.text_input("Weight (kg)", value="", key="weight_years")
        with col2:
            allergies = st.text_area("Allergies or Sensitivities", value="None", height=100, key="allergies_years")
            health_notes = st.text_area("Medical History/Notes", value="None", height=100, key="health_notes_years")
        
        goals = st.multiselect(
            "Your Parenting Goals 🌟 (Select all that apply)",
            options=PARENTING_GOALS,
            default=["General care and well-being"],
            key="goals_years"
        )

        submitted = st.form_submit_button("Generate Guide 🎉")

    if submitted:
        if not name:
            st.error("Please enter your baby’s name! 👶")
        elif not weight:
            st.error("Please enter your baby’s weight! ⚖️")
        else:
            goals_str = ", ".join(goals) if goals else "None selected"
            baby_profile = f"""
            Name: {name}
            Age: {age_years} years
            Gender: {gender}
            Weight: {weight} kg
            Allergies: {allergies}
            Health Notes: {health_notes}
            Parenting Goals: {goals_str}
            """

            st.markdown("---")
            st.subheader(f"🍼 Care Guide for {name}")

            with st.spinner("Crafting your baby’s guide... 🌟"):
                guide = generate_baby_guide(baby_profile, "years")

            if isinstance(guide, dict) and "error" in guide:
                st.markdown(f"<div class='card'><b>Oops! 😢</b> {guide['error']}</div>", unsafe_allow_html=True)
            else:
                with st.expander("View Your Baby’s Guide 🌈", expanded=True):
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🍼 1. Feeding</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Timing: {guide['feeding']['timing']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Quantity: {guide['feeding']['quantity']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Foods: {guide['feeding']['foods']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🌙 2. Sleeping Routines</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Total Hours: {guide['sleeping_routines']['total_hours']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Routine: {guide['sleeping_routines']['routine']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>⭐ 3. Milestone Tracking</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Age-Specific Milestones: {guide['milestone_tracking']['age_specific_milestones']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>⏰ 4. Daily Schedule</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Schedule: {guide['daily_schedule']['schedule']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🩺 5. Health Concerns</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Concerns: {guide['health_concerns']['concerns']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Tips: {guide['health_concerns']['tips']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>💕 6. Emotional Bonding</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Bonding: {guide['emotional_bonding']['bonding']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Development: {guide['emotional_bonding']['development']}</div>", unsafe_allow_html=True)
                    st.markdown("<b class='json-section'>🌟 7. Parenting Tips</b>", unsafe_allow_html=True)
                    st.markdown(f"<div class='json-content'>Tips: {guide['parenting_tips']['tips']}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                pdf_buffer = generate_pdf(guide, name)
                st.download_button(
                    label="Download Guide (PDF) 📑",
                    data=pdf_buffer,
                    file_name=f"{name}_baby_care_guide.pdf",
                    mime="application/pdf"
                )

# Footer
st.markdown("---")
st.markdown('<div class="footer">Powered by Google Gemini • Built with Streamlit<br>Developed by Amresh Yadav • maithilgeek@gmail.com</div>', unsafe_allow_html=True)