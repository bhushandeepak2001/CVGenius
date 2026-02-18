🚀 CVGenius Resume Builder

An intelligent resume optimization platform that enhances resumes using AI (OpenAI + Gemini APIs) and calculates ATS compatibility scores based on target job descriptions.

📌 Features

✨ AI-based grammar and phrasing improvement

🎯 Job-description keyword optimization

📊 ATS score calculation (before & after enhancement)

🧠 Intelligent skill and keyword extraction

📄 Resume upload (PDF/DOCX) support

🖥 Interactive UI built with Streamlit

🏗 Tech Stack

Frontend:

Streamlit

Backend:

FastAPI

Python

AI Integration:

OpenAI API

Google Gemini API

📊 How ATS Score Works

The system:

Extracts keywords from the target job description

Matches them with resume content

Calculates keyword density & semantic similarity

Generates:

Initial ATS Score

Enhanced ATS Score

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/yourusername/ai-ats-resume-builder.git
cd ai-ats-resume-builder

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add OpenAI API Key

You can either:

Option A (Recommended - Environment Variable)

setx OPENAI_API_KEY "your_api_key_here"


OR

Option B (Direct in Code)

client = OpenAI(api_key="your_api_key_here")

4️⃣ Run Backend
uvicorn main:app --reload

5️⃣ Run Frontend
streamlit run app.py

📂 Project Structure
├── main.py              # FastAPI backend
├── app.py               # Streamlit frontend
├── requirements.txt
├── utils/               # ATS scoring & AI logic
└── README.md

🎯 Use Case

Students applying for internships

Professionals switching jobs

Resume optimization for ATS-based hiring systems

🔥 Future Improvements

Resume PDF export

Multiple resume templates

Job scraping integration

Dashboard with resume analytics
