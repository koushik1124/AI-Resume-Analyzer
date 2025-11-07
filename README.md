# 🤖 AI Resume Analyzer (DeepSeek V3.1)

An **AI-powered Resume Analyzer** built with **Python**, **Streamlit**, and **DeepSeek V3.1 (via OpenRouter)** that automatically extracts, analyzes, and improves resumes.  
Upload your PDF or Word resume to get instant insights, role recommendations, and personalized AI feedback.

---

## 🌟 Features

✅ Extracts key information from resumes (Email, Skills, etc.)  
✅ Recommends best-fit roles based on skill match percentage  
✅ Calculates a weighted Resume Score (0–100)  
✅ Provides AI-powered improvement suggestions (DeepSeek V3.1)  
✅ Handles PDFs (with OCR fallback for scanned resumes) & DOCX files  
✅ Clean dashboard with interactive visualizations  

---

## 🧩 Tech Stack

| Category | Technology |
|-----------|-------------|
| Frontend | Streamlit |
| Backend | Python, spaCy, pandas |
| AI Model | DeepSeek V3.1 via OpenRouter |
| NLP & Parsing | PyMuPDF, pytesseract, docx2txt |
| Visualization | Plotly |
| Environment | dotenv, virtualenv |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/<your-username>/ai-resume-analyzer.git
cd ai-resume-analyzer
2️⃣ Create a virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate   # (Windows)
# or
source venv/bin/activate  # (Mac/Linux)
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Add your API key in .env
Create a .env file in the project root and add:

ini
Copy code
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
🧠 Get your API key from OpenRouter.

🖥️ Run the Application
bash
Copy code
cd frontend
streamlit run app.py
Then open http://localhost:8501 in your browser.

📂 Project Structure
graphql
Copy code
ai-resume-analyzer/
│
├── backend/
│   ├── analyze.py          # NLP, email/skills extraction, scoring
│   ├── extract.py          # Text extraction from PDF/DOCX (OCR support)
│   ├── ai_helper.py        # AI feedback via DeepSeek V3.1 (OpenRouter)
│
├── frontend/
│   └── app.py              # Streamlit dashboard & user interface
│
├── data/
│   ├── skills.csv          # Predefined list of skills
│   └── job_roles.json      # Skill-based job role mapping
│
├── .env                    # Contains API key (not uploaded)
├── .gitignore
├── requirements.txt
└── README.md
📊 Dashboard Overview
📧 Email Extraction: Detects valid email IDs, even from noisy PDFs

🧠 Skill Detection: Identifies matching skills from a CSV knowledge base

💼 Role Recommendation: Suggests most relevant job role

⭐ Resume Score: Quantifies profile strength

🤖 AI Feedback: DeepSeek V3.1 provides tailored suggestions for improvement

🧠 Powered by DeepSeek V3.1
This app integrates DeepSeek V3.1 through the OpenRouter API to deliver contextual feedback, strengths, weaknesses, and improvement suggestions for your resume.

🧾 Example Output
Example:
Recommended Role: Data Analyst
Resume Score: 84/100
AI Feedback:

“This resume demonstrates strong technical and analytical skills.
Consider adding measurable results and a project summary to enhance impact.”

💡 Future Enhancements
 Add job title dropdown to compare against target role

 Export resume analysis as downloadable PDF

 Add sidebar analytics dashboard

 Integrate Gemini / GPT API fallback

 Enhance OCR for image-based resumes

📜 License
MIT License © 2025 Koushik
Feel free to fork, modify, and improve this project!

⭐ Support
If you found this project helpful, give it a ⭐ on GitHub
and share it with your peers!
