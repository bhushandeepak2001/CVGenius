from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
import shutil
import os
import re
import requests

app = FastAPI()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key="")


# ==============================
# Resume Data Model
# ==============================

class ResumeData(BaseModel):
    personal_info: dict
    education: list
    skills: list
    experience: list
    projects: list
    target_job_description: str = ""


# ==============================
# Home Route
# ==============================

@app.get("/")
def home():
    return {"message": "AI ATS Resume Builder API Running"}


# ==============================
# Resume Upload
# ==============================

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    try:
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "filename": file.filename
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# ==============================
# ATS SCORING FUNCTION
# (If you don't have Free ATS API,
# we simulate a real keyword match)
# ==============================

def calculate_ats_score(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    resume_words = set(re.findall(r'\b\w+\b', resume_text))
    job_words = set(re.findall(r'\b\w+\b', job_description))

    stopwords = {"the", "and", "is", "in", "to", "of", "a", "for", "with", "on", "as"}
    job_words = job_words - stopwords

    if len(job_words) == 0:
        return 0

    matched_keywords = resume_words.intersection(job_words)

    score = (len(matched_keywords) / len(job_words)) * 100

    return round(score, 2)


# ==============================
# Generate Resume Route
# ==============================

@app.post("/generate-resume/")
def generate_resume(data: ResumeData):

    # Step 1 — Convert structured data to text
    resume_text = f"""
    Personal Info: {data.personal_info}
    Education: {data.education}
    Skills: {data.skills}
    Experience: {data.experience}
    Projects: {data.projects}
    """

    # Step 2 — Initial ATS Score
    initial_score = calculate_ats_score(
        resume_text,
        data.target_job_description
    )

    # Step 3 — AI Enhancement (OpenAI)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional resume optimizer. Improve grammar, add measurable achievements, optimize keywords, and maintain professional tone."
            },
            {
                "role": "user",
                "content": f"""
                Improve and optimize this resume for the following job description:

                JOB DESCRIPTION:
                {data.target_job_description}

                RESUME:
                {resume_text}
                """
            }
        ],
        temperature=0.4
    )

    enhanced_resume = response.choices[0].message.content

    # Step 4 — Final ATS Score (after AI)
    final_score = calculate_ats_score(
        enhanced_resume,
        data.target_job_description
    )

    return {
        "initial_ats_score": initial_score,
        "final_ats_score": final_score,
        "enhanced_resume": enhanced_resume
    }
