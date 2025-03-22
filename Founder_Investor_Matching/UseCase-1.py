# Import Streamlit for creating the web app interface
import streamlit as st
# Import Google Gemini AI for compatibility analysis
import google.generativeai as genai
# Import json for handling JSON data
import json
# Import re for regular expression text preprocessing
import re
# Import os for file path handling
import os
# Import pandas for CSV handling
import pandas as pd

# 🔹 Configure Gemini API
genai.configure(api_key="AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0")  # Replace with your actual API key
GEMINI_MODEL = "models/gemini-1.5-flash-001-tuning"  # Defines the specific Gemini model

# 🔹 Initial Investor Dataset
INVESTOR_DATA = []  # Initializes an empty list for investor data

# 🔹 Session State Initialization
if 'match_results' not in st.session_state:
    st.session_state['match_results'] = None

# Define a default value for max_results
MAX_RESULTS_DEFAULT = 10

# 🔹 Compatibility Analysis Functions
def analyze_compatibility_gemini(founder_data, investor_data):
    """
    Analyzes compatibility between a founder and an investor using Gemini AI.
    Args:
        founder_data (dict): Data about the founder's startup
        investor_data (dict): Data about the investor's preferences
    Returns:
        tuple: (match_score, reasoning) or (0, error_message) if analysis fails
    """
    try:
        prompt = (
            f"Evaluate the compatibility between a startup founder and an investor based on the following data:\n"
            f"Founder Data: Industry: {founder_data.get('industry', 'Unknown')}, Stage: {founder_data.get('stage', 'Unknown')}, "
            f"Funding Required: ${founder_data.get('funding_required', 'Unknown')}, Traction: {founder_data.get('traction', 'Unknown')}, "
            f"Business Model: {founder_data.get('business_model', 'Unknown')}\n"
            f"Investor Preferences: Preferred Industry: {investor_data.get('Industry', 'Unknown')}, "
            f"Investment Range: {investor_data.get('Cheque_range', 'Unknown')}, Preferred Stage: {investor_data.get('Stage', 'Unknown')}, "
            f"Countries: {investor_data.get('Countries', 'Unknown')}\n"
            "Return a valid JSON object in this format:\n"
            "```json\n"
            "{\n"
            '  "match_score": <integer between 0-100>,\n'
            '  "reasoning": "<Explanation of compatibility>"\n'
            "}\n"
            "```\n"
        )
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        json_match = re.search(r'```json\n(.*?)\n```', response.text.strip(), re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
            return result.get("match_score", 0), result.get("reasoning", "No reasoning provided.")
        else:
            return 0, "Evaluation failed: Invalid response format from Gemini AI."
    except genai.GenerationError as ge:
        st.error(f"❌ Gemini API generation error: {ge}")
        return 0, f"Evaluation failed due to Gemini API error: {str(ge)}"
    except json.JSONDecodeError as je:
        st.error(f"❌ JSON parsing error: {je}")
        return 0, f"Evaluation failed due to invalid JSON format: {str(je)}"
    except Exception as e:
        st.error(f"❌ Unexpected error in compatibility analysis: {e}")
        return 0, f"Evaluation failed due to unexpected error: {str(e)}"

def calculate_matches(founder_data, investors_list, min_score, max_results):
    """
    Calculates matches between founder data and a list of investors.
    Args:
        founder_data (dict): Founder's startup data
        investors_list (list): List of investor dictionaries
        min_score (int): Minimum compatibility score to include
        max_results (int): Maximum number of matches to return
    Returns:
        list: Sorted list of matches or empty list if no investors
    """
    try:
        if not investors_list:
            st.error("Upload the investor data first")
            return []
        matches = []
        for investor in investors_list:
            score, reasoning = analyze_compatibility_gemini(founder_data, investor)
            if score >= min_score:
                matches.append({
                    "investor_name": investor.get("Name", "Unknown Investor"),
                    "match_score": score,
                    "reasoning": reasoning
                })
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches[:max_results]
    except Exception as e:
        st.error(f"❌ Error calculating matches: {e}")
        return []

# 🔹 Sidebar Functionality
with st.sidebar:
    st.markdown("### ⚙️ Model Settings")
    st.write("Configure the matching process:")
    
    min_score = st.slider("Minimum Match Score", 0, 100, 70, help="Set the minimum compatibility score to filter investors.")
    
    st.markdown("### 📊 Investor Dataset")
    investor_upload = st.file_uploader("Upload Investor Dataset (JSON)", type=["json"])
    if investor_upload:
        try:
            INVESTOR_DATA = json.load(investor_upload)
            st.success("Investor dataset uploaded successfully!")
            st.write(f"Loaded {len(INVESTOR_DATA)} investors")
        except json.JSONDecodeError as e:
            st.error(f"❌ Failed to parse investor dataset: Invalid JSON format - {e}")
        except Exception as e:
            st.error(f"❌ Failed to parse investor dataset: {e}")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write("AI-powered founder-investor matching using Google Gemini with data from Vertx dataset.")
    st.write(f"Current Date: March 21, 2025")

# 🔹 Main UI
st.markdown('<div class="main-title">Founder-Investor Matching AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the Perfect Investor for Your Startup</div>', unsafe_allow_html=True)

with st.container():
    st.markdown("### Enter Founder Profile")
    founder_data = {
        "name": st.text_input("Startup Name", "My Startup"),
        "industry": st.selectbox("Industry", ["Tech", "Healthcare", "Energy", "Fintech", "SaaS", "Other"]),
        "stage": st.selectbox("Startup Stage", ["Pre-Seed", "Seed", "Series A", "Series+"]),
        "funding_required": st.number_input("Funding Required ($)", min_value=0, value=100000, step=10000),
        "traction": st.text_input("Traction", "e.g., 10K users, $50K revenue"),
        "business_model": st.selectbox("Business Model", ["SaaS", "Subscription", "B2B", "B2C", "Other"])
    }

    if st.button("Find Matches", use_container_width=True) and founder_data:
        with st.spinner("Analyzing investor matches..."):
            matches = calculate_matches(founder_data, INVESTOR_DATA, min_score, MAX_RESULTS_DEFAULT)
            if matches:
                st.session_state['match_results'] = {
                    "founder_name": founder_data.get("name", "Uploaded Founder"),
                    "matches": matches
                }
            else:
                st.session_state['match_results'] = None
                st.error("❌ Please try later.")

# Display match results if they exist
if st.session_state['match_results']:
    results = st.session_state['match_results']
    st.success(f"🎉 Matches Found for {results['founder_name']}")
    st.markdown("### Investor Matches")
    for match in results['matches']:
        with st.expander(f"💼 {match['investor_name']} - Score: {match['match_score']}/100", expanded=False):
            st.markdown(f"""
                <div class="card">
                    <span class="score">Match Score: {match['match_score']}/100</span><br>
                    <span class="feedback"><strong>Reasoning:</strong> {match['reasoning']}</span>
                </div>
            """, unsafe_allow_html=True)
    
    # Prepare data for CSV and JSON
    matches_df = pd.DataFrame(results['matches'])
    matches_json = json.dumps(results['matches'], indent=2)
    csv_file_name = f"{results['founder_name'].replace(' ', '_')}_investor_matches.csv"
    json_file_name = f"{results['founder_name'].replace(' ', '_')}_investor_matches.json"

    # Save buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save as CSV"):
            csv_output_path = os.path.join(os.getcwd(), csv_file_name)
            try:
                matches_df.to_csv(csv_output_path, index=False)
                st.success(f"CSV results saved to: `{csv_output_path}`")
            except Exception as e:
                st.error(f"Failed to save CSV file locally: {e}")
    
    with col2:
        if st.button("Save as JSON"):
            json_output_path = os.path.join(os.getcwd(), json_file_name)
            try:
                with open(json_output_path, 'w', encoding='utf-8') as f:
                    f.write(matches_json)
                st.success(f"JSON results saved to: `{json_output_path}`")
            except Exception as e:
                st.error(f"Failed to save JSON file locally: {e}")

    


st.markdown("---")
st.markdown('<div style="text-align: center; color: #78909C;">Powered by Google Gemini • Built with Streamlit</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #78909C;">Developed By Amresh Yadav • Email Id: maithilgeek@gmail.com, Mob. - 7260905948</div>', unsafe_allow_html=True)

# 🔹 Optional CSS for Styling
st.markdown("""
    <style>
    .main-title { font-size: 2.5em; font-weight: bold; color: #1E88E5; text-align: center; }
    .subtitle { font-size: 1.2em; color: #78909C; text-align: center; margin-bottom: 20px; }
    .card { padding: 10px; border: 1px solid #E0E0E0; border-radius: 5px; background-color: #F9F9F9; }
    .score { font-weight: bold; color: #1E88E5; }
    .feedback { color: #424242; }
    </style>
""", unsafe_allow_html=True)