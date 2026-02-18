import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CVGenius Resume Builder", layout="wide")

st.title("🚀 CVGenius Resume Builder")

# -----------------------------
# OPTION SELECTION
# -----------------------------
option = st.radio(
    "Choose Input Method",
    ["Upload Resume", "Manual Entry"],
    horizontal=True
)

# ======================================================
# OPTION 1: Upload Resume
# ======================================================
if option == "Upload Resume":

    st.subheader("📤 Upload Your Resume")

    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"]
    )

    # job_description_upload = st.text_area("🎯 Target Job Description")

    if uploaded_file is not None:

        files = {"file": uploaded_file}
        response = requests.post(f"{API_URL}/upload-resume/", files=files)

        if response.status_code == 200:
            st.success("Resume uploaded successfully!")

            # Now call generate endpoint
            generate_response = requests.post(
                f"{API_URL}/generate-resume/",
                json={
                    "personal_info": {},
                    "education": [],
                    "skills": [],
                    "experience": [],
                    "projects": [],
                    "target_job_description": job_description_upload
                }
            )

            if generate_response.status_code == 200:
                data = generate_response.json()

                st.subheader("📊 ATS Score Analysis")

                col1, col2 = st.columns(2)

                col1.metric("Initial ATS Score", data["initial_ats_score"])
                col2.metric(
                    "Final ATS Score",
                    data["final_ats_score"],
                    delta=data["final_ats_score"] - data["initial_ats_score"]
                )

                st.subheader("✨ AI Enhanced Resume")
                st.text_area(
                    "Enhanced Resume Output",
                    data["enhanced_resume"],
                    height=400
                )

            else:
                st.error("Failed to calculate ATS score.")
        else:
            st.error("Upload failed.")


# ======================================================
# OPTION 2: Manual Entry
# ======================================================
if option == "Manual Entry":

    st.subheader("✍️ Enter Your Details")

    with st.form("manual_form"):

        st.markdown("### 👤 Personal Information")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        st.markdown("### 🎓 Education")
        education = st.text_area("Education Details")

        st.markdown("### 🛠 Skills & Certifications")
        skills = st.text_area("Skills (comma separated)")
        certifications = st.text_area("Certifications")

        st.markdown("### 💼 Work Experience")
        experience = st.text_area("Work Experience")

        st.markdown("### 🚀 Projects & Achievements")
        projects = st.text_area("Projects & Achievements")

        st.markdown("### 🎯 Target Job Description")
        job_description = st.text_area("Job Description")

        submit = st.form_submit_button("Generate Resume")

    if submit:

        payload = {
            "personal_info": {
                "name": name,
                "email": email,
                "phone": phone
            },
            "education": [education],
            "skills": skills.split(","),
            "experience": [experience],
            "projects": [projects],
            "target_job_description": job_description
        }

        response = requests.post(
            f"{API_URL}/generate-resume/",
            json=payload
        )

        if response.status_code == 200:

            data = response.json()

            st.success("Resume Generated Successfully!")

            st.subheader("📊 ATS Score Analysis")

            col1, col2 = st.columns(2)

            col1.metric("Initial ATS Score", data["initial_ats_score"])
            col2.metric(
                "Final ATS Score",
                data["final_ats_score"],
                delta=data["final_ats_score"] - data["initial_ats_score"]
            )

            st.subheader("✨ AI Enhanced Resume")
            st.text_area(
                "Enhanced Resume Output",
                data["enhanced_resume"],
                height=400
            )

        else:
            st.error("Something went wrong.")
