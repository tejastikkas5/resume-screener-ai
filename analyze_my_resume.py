import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
import PyPDF2 as pdf

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

def main():
    st.title("Resume Analyzer AI")
    st.header("Optimize Your Resume, Maximize Your Chances")




    def get_gemini_response(input_text):
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(input_text)
        return response.text


    def input_pdf_text(uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += str(page.extract_text())
        return text


    jd = st.text_area("Enter Job Description Here...")
    uploaded_file = st.file_uploader(
        "Upload Your Resume", type="pdf", help="Upload Resume PDF only"
    )

    submit1 = st.button("Tell Me About the Resume")
    submit2 = st.button("Suggestion to improve my Skills")
    submit3 = st.button("Optimize My Resume for ATS")
    submit4 = st.button("Find Best-Suited Jobs for Me ")
    submit5 = st.button("Mock Interview Question")


    input_prompt1 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. Your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    First the output should come as Match percentage and then the keywords missing and then strengths and weaknesses of the applicant in relation to the specified job requirements and last final thoughts and the recommendation. Dont reply like an ai like Okay, here's a breakdown of the resume against the job description, as an ATS scanner would analyze it
    """

    input_prompt2 = """
    You are a skilled ATS (Applicant Tracking System) scanner with deep expertise in evaluating resumes and job descriptions. Your task is to analyze the provided resume and identify key areas for skill improvement based on the job market trends and the candidate’s target roles. 

    Your response should follow this structured format:
    1. **Skill Gaps:** Identify the missing or underdeveloped skills crucial for career advancement.
    2. **Industry Trends:** Highlight relevant skills or technologies currently in demand for the candidate’s field.
    3. **Personalized Learning Path:** Recommend practical ways to acquire these skills (courses, certifications, projects, etc.).
    4. **Final Suggestions:** Summarize the most crucial skills to focus on and propose an actionable plan for enhancing the candidate’s employability.

    Ensure the feedback is Brief, specific, and actionable, avoiding generic responses. Tailor the suggestions to the candidate’s profile and career aspirations.Dont reply like an ai like Okay, let's analyze Tejas Tikkas' resume and provide tailored feedback to improve his chances of landing a Python Developer Internship, specifically targeting roles similar to the Inlighn Tech internship he is considering.
    """


    input_prompt3 = """
    You are an expert ATS (Applicant Tracking System) optimizer with deep knowledge of resume screening algorithms. Your task is to analyze the provided resume and suggest improvements to enhance its ATS compatibility.

    Your response should include:
    1. **ATS Score:** Evaluate how well the resume is optimized for ATS parsing.
    2. **Formatting Issues:** Identify any structural or design elements that may reduce ATS readability.
    3. **Keyword Optimization:** Suggest important keywords and phrases to improve ranking in ATS filters.
    4. **Content Enhancement:** Recommend changes to make the resume more impactful and aligned with job market trends.
    5. **Final Recommendations:** Summarize the key changes needed for better ATS performance.

    Ensure the feedback specific, actionable, and focused on maximizing ATS visibility.Dont reply like an ai like Alright, let's analyze this resume and optimize it for ATS based on the Python Developer Internship job description provided.
    """


    input_prompt4 = """
    You are an intelligent career advisor with expertise in job market analysis. Your task is to analyze the provided resume and suggest the best-suited job roles based on the candidate’s skills, experience, and industry trends.

    Your response should include:
    1. **Top Matching Job Roles:** List job titles that align well with the candidate’s qualifications.
    2. **Industry Fit:** Identify the industries or sectors where the candidate is most likely to succeed.
    3. **Skill-Based Suggestions:** Recommend job roles based on the candidate’s strongest skills.
    4. **Career Growth Opportunities:** Provide insights on roles that could help the candidate advance in their career.
    5. **Final Recommendation:** Summarize the most suitable job roles and suggest possible next steps for job applications.

    Ensure the feedback is specific, practical, and tailored to the candidate’s profile. Dont reply like an ai like Alright, Okay, let's break down Tejas's resume and pinpoint the best career paths and how to approach a specific internship opportunity. or Here's an analysis of Tejas's resume and career prospects, along with targeted advice for the Python Developer Internship at Inlighn Tech:
    """


    input_prompt5 = """
    You are an AI-powered interview coach with expertise in analyzing resumes and generating job-specific interview questions. Your task is to conduct a mock interview based on the provided resume, focusing on the candidate’s skills, experience, and target roles.

    Your response should include:
    1. **Personalized Interview Questions:** Generate relevant questions based on the candidate’s resume and industry.
    2. **Behavioral & Technical Questions:** Include a mix of HR (behavioral) and role-specific technical questions.
    3. **Expected Answer Insights:** Provide brief guidance on what an ideal response should include.
    4. **Areas to Improve:** Identify potential weaknesses in the resume that could be questioned in an interview.
    5. **Final Recommendations:** Offer tips on how the candidate can better prepare for interviews.

    Ensure the questions are tailored, realistic, and align with industry standards.Dont reply like an ai like Okay, Tejas, let's get started with this mock interview. I'll be focusing on the Python Developer Internship at Inlighn Tech, based on your resume. Remember to be concise, enthusiastic, and confident in your responses. just start the question and answers   
    """


    if submit1:
        if uploaded_file is not None and jd.strip():
            pdf_content = input_pdf_text(uploaded_file)
            formatted_prompt = (
                input_prompt1 + "\nResume:\n" + pdf_content + "\nJob Description:\n" + jd
            )
            response = get_gemini_response(formatted_prompt)
            st.subheader("The Response is:")
            st.write(response)  
        else:
            st.error("Please upload the resume and enter a job description.")

    if submit2:
        if uploaded_file is not None and jd.strip():
            pdf_content = input_pdf_text(uploaded_file)
            formatted_prompt = (
                input_prompt2 + "\nResume:\n" + pdf_content + "\nJob Description:\n" + jd
            )
            response = get_gemini_response(formatted_prompt)
            st.subheader("The Response is:")
            st.write(response) 
        else:
            st.error("Please upload the resume and enter a job description.")

    if submit3:
        if uploaded_file is not None and jd.strip():
            pdf_content = input_pdf_text(uploaded_file)
            formatted_prompt = (
                input_prompt3 + "\nResume:\n" + pdf_content + "\nJob Description:\n" + jd
            )
            response = get_gemini_response(formatted_prompt)
            st.subheader("The Response is:")
            st.write(response) 
        else:
            st.error("Please upload the resume and enter a job description.")

    if submit4:
        if uploaded_file is not None and jd.strip():
            pdf_content = input_pdf_text(uploaded_file)
            formatted_prompt = (
                input_prompt4 + "\nResume:\n" + pdf_content + "\nJob Description:\n" + jd
            )
            response = get_gemini_response(formatted_prompt)
            st.subheader("The Response is:")
            st.write(response) 
        else:
            st.error("Please upload the resume and enter a job description.")

    if submit5:
        if uploaded_file is not None and jd.strip():
            pdf_content = input_pdf_text(uploaded_file)
            formatted_prompt = (
                input_prompt5 + "\nResume:\n" + pdf_content + "\nJob Description:\n" + jd
            )
            response = get_gemini_response(formatted_prompt)
            st.subheader("The Response is:")
            st.write(response) 
        else:
            st.error("Please upload the resume and enter a job description.")



