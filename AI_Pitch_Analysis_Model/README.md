
# AI Pitch Deck Analyzer

An AI-powered web application built with Streamlit and Google Gemini to analyze startup pitch decks. Extract insights, evaluate key sections, and generate detailed feedback to improve your pitch.

---

## ✨ Features

- **Flexible Input**: Upload a PDF pitch deck or provide a URL (e.g., Google Drive, GitHub).
- **Section Analysis**: Evaluates six critical sections:
  - Problem
  - Solution
  - Market
  - Business Model
  - Financials
  - Team
- **Customizable Weights**: Adjust the importance of each section to suit your analysis needs.
- **AI-Powered Insights**: Uses Google Gemini for text extraction and section evaluation.
- **OCR Support**: Extracts text from scanned PDFs using Tesseract OCR when standard parsing fails.
- **Detailed Feedback**: Provides scores, strengths, weaknesses, and suggestions for each section.
- **Downloadable Results**: Export analysis results as a text file.
- **Enhanced UI**: Modern, user-friendly interface with custom CSS styling.

---

## 🛠️ Technologies Used

- **Streamlit**: Web app interface.
- **Google Gemini**: AI model for text extraction and evaluation.
- **pdfplumber**: PDF text extraction.
- **pytesseract**: OCR for scanned PDFs.
- **PIL (Pillow)**: Image processing for OCR.
- **requests**: Fetching PDFs from URLs.
- **re**: Text preprocessing with regular expressions.
- **BytesIO**: In-memory handling of PDF files.

---

## 📋 Prerequisites

1. **Python 3.8+**: Ensure Python is installed.
2. **Google Gemini API Key**: Obtain an API key and replace the placeholder in the code (`"AIzaSyDwLiS2uHId79Lhn2mwdr7dhNHZXYoHZl0"`).
3. **Tesseract OCR**: Install Tesseract for OCR support (required for scanned PDFs):
   - Windows: Download and install from [Tesseract](https://github.com/tesseract-ocr/tesseract).
   - Linux/macOS: `sudo apt-get install tesseract-ocr` or `brew install tesseract`.

---

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ai-pitch-deck-analyzer.git
   cd ai-pitch-deck-analyzer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `requirements.txt`**:
   
   ```
   streamlit
   pdfplumber
   requests
   google-generativeai
   pytesseract
   Pillow
   ```

4. **Set Up API Key**:
   Replace the placeholder API key in the code with your Google Gemini API key.

5. **Run the App**:
   ```bash
   streamlit run app.py
   ```

---

## 📖 Usage

1. **Launch the App**: Run the script and open the provided local URL (e.g., `http://localhost:8501`) in your browser.
2. **Choose Input Method**:
   - Upload a PDF pitch deck.
   - Enter a URL to a publicly accessible PDF (supports Google Drive and GitHub links).
3. **Adjust Weights**: Use the sidebar sliders to customize section weights (optional).
4. **Analyze**: Click "Analyze PDF" or "Analyze URL" to process the deck.
5. **View Results**: See the total score, section-by-section feedback, and download the results as a text file.

---

## 📑 Code Structure

- **`usecase2.py`**: Main application script with all logic.
  - **Text Extraction**: Functions for PDF parsing and OCR.
  - **Section Analysis**: Gemini-based section extraction and evaluation.
  - **UI**: Streamlit interface with custom CSS and sidebar settings.

---

## 🔧 Customization

- **Weights**: Modify `DEFAULT_WEIGHTS` to change default section importance.
- **Criteria**: Update `CRITERIA` to adjust evaluation metrics.
- **Styling**: Edit the CSS in `st.markdown` for a different look and feel.

---

## ⚠️ Limitations

- Requires a valid Google Gemini API key.
- OCR may struggle with low-quality scans or complex layouts.
- URL fetching supports only Google Drive and GitHub PDFs (customize `fetch_pdf_from_url` for more).
- Internet connection required for API calls and URL fetching.

---

## 👨‍💻 Developer

- **Name**: Amresh Yadav
- **Email**: maithilgeek@gmail.com
- **Mobile**: +91 7260905948

---



## 🌟 Acknowledgments

- Powered by [Google Gemini](https://cloud.google.com/gemini).
- Built with [Streamlit](https://streamlit.io/).
- OCR support by [Tesseract](https://github.com/tesseract-ocr/tesseract).

