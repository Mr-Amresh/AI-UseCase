
# 👶 Baby Care Assistant

A personalized baby care guide generator built with **Streamlit** and powered by **Google Gemini API**. This application helps new parents create tailored care plans for their babies based on age, weight, allergies, and parenting goals. The guide is presented in an interactive web interface and can be downloaded as a PDF.

---

## ✨ Features

- Personalized baby care guide generation based on specific baby details
- Age input support in months (0–36) or years (0–3)
- Interactive and baby-themed Streamlit UI
- PDF export of the generated guide
- Health recommendations aligned with pediatric best practices
- Visually appealing UI with custom fonts and hover effects

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** – for building the web interface
- **Google Gemini API** – for generating AI-powered content
- **ReportLab** – for generating PDF reports
- **CSS** – for custom styling

---

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud account with Gemini API enabled
- Gemini API Key
- Git (optional)

---

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/baby-care-assistant.git
cd baby-care-assistant
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your API key in `app.py`:

```python
genai.configure(api_key="your-actual-api-key")
```

---

## 📂 Project Structure

```
baby-care-assistant/
├── app.py
├── requirements.txt
├── README.md
└── venv/ (optional)
```

---

## 📦 Requirements

```
streamlit==1.36.0
google-generativeai==0.7.2
reportlab==4.2.2
```

Install with:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## 🌟 Example Usage

- **Name**: Emma  
- **Age**: 6 months  
- **Gender**: Girl  
- **Weight**: 7 kg  
- **Allergies**: None  
- **Health Notes**: Healthy, occasional fussiness  
- **Goals**: Establish sleep routine, introduce solids

Click **"Generate Guide 🎉"** and download the guide as `Emma_baby_care_guide.pdf`.

---

## 🛠️ Troubleshooting

- **Invalid API Response**: Verify API key and model (`gemini-1.5-flash`)
- **PDF Errors**: Check if `reportlab` is installed properly
- **App Won’t Start**: Ensure Streamlit is correctly installed and port 8501 is open

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature/feature-name`
5. Open a Pull Request

---

## 📜 License

Licensed under the **MIT License**. See [LICENSE](LICENSE) for more info.

---

## 🙌 Credits

- **Developer**: Amresh Yadav  
- **Email**: [maithilgeek@gmail.com](mailto:maithilgeek@gmail.com)  
- **Powered By**: Google Gemini API & Streamlit

---

## 🌈 Future Plans

- Add multi-language support
- Display milestone visual charts
- Integrate real-time pediatric data
- Enhance PDF layout with illustrations and color themes
