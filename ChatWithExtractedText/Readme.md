
# Chat Assistant with Image Extractor 🤖🖼️

An intelligent chatbot powered by Google Gemini, enhanced with OCR capabilities to extract text from images and continue conversations with contextual awareness.

---

## 🚀 Features

- **Conversational Chatbot**: Engage with a Gemini-powered AI that remembers your conversation context.
- **Model Selection**: Easily switch between Gemini models (`gemini-1.5-flash-001-tuning`, `gemini-1.5-pro`, `gemini-1.0-pro`).
- **Image Text Extraction**: Upload JPG/PNG images and extract text using Tesseract OCR, with a confidence score.
- **Dynamic Input**: Type new queries after each response; the input field resets automatically.
- **Chat History**: Styled interface showing past messages between the user and bot.
- **Extracted Text Queries**: Use OCR-extracted content as input to the chatbot for context-aware replies.

---

## 📦 Prerequisites

- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chat-assistant-with-image-extractor.git
cd chat-assistant-with-image-extractor
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit google-generativeai Pillow pytesseract pandas
```

### 3. Install Tesseract OCR

- **Windows**: [Download and install Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Update the script path if needed (default: `C:\Program Files\Tesseract-OCR\tesseract.exe`).
- **Linux**:

```bash
sudo apt-get install tesseract-ocr
```

- **macOS**:

```bash
brew install tesseract
```

---

## 🔑 Set Up Gemini API Key

1. Get your API key from [Google Gemini](https://ai.google.dev/).
2. Enter it in the sidebar of the app or hardcode it in the script (not recommended for security).

---

## 🧠 Usage

### Run the App

```bash
streamlit run chatbot_with_image.py
```

### Interact with the Chatbot

- Open [http://localhost:8501](http://localhost:8501)
- Enter your query and click **"Send 🚀"**
- Input clears after each response
- Upload an image under **"Image Text Extractor"** in the sidebar
- View extracted text and confidence score
- Click **"Send Extracted Text 📸"** to query based on the image content

---

## 🗂️ Project Structure

```
chat-assistant-with-image-extractor/
│
├── chatbot_with_image.py     # Main application file
├── requirements.txt          # Dependencies list
└── README.md                 # Project documentation
```

---

## 💡 Example Usage

1. **Text Query**
   - Input: `"What is machine learning?"`
   - Output: `"Machine learning is a subset of AI where systems learn from data..."`

2. **Follow-up Query**
   - Input: `"Tell me more."`
   - Output: Further explanation based on previous context.

3. **Image Query**
   - Upload image with text `"Python basics"`
   - Extracted Text: `"Python basics"` (Confidence: 92.34%)
   - Chatbot responds with explanation of Python basics

---

## ⚠️ Notes

- **Chat Memory**: The bot maintains conversation context, limited by Gemini’s token cap.
- **OCR Confidence**: Score range 0–100%; values <50% will display a warning.
- **Tesseract Path**: Update `pytesseract.pytesseract.tesseract_cmd` in the script if needed.

---

## 🛠️ Troubleshooting

- **Tesseract Not Found**: Ensure it's installed and the path is correctly configured.
- **API Key Errors**: Confirm the key is valid and has access to selected models.
- **No Response**: Check your internet connection and model availability.

---

## 🤝 Contributing

Contributions are welcome! Fork the repo, open issues, or submit pull requests.

---


## 👨‍💻 Author

**Amresh Yadav**  
📧 Email: [maithilgeek@gmail.com](mailto:maithilgeek@gmail.com)  


---



