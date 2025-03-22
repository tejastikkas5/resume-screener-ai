import streamlit as st
import pandas as pd
import re
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import google.generativeai as genai
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import streamlit as st
import threading 
import smtplib


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

EMAIL_ADDRESS = os.getenv("MAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def main():

    def extract_text_from_pdf(pdf_file):
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text

    
    def extract_text_from_docx(docx_file):
        doc = Document(docx_file)
        return "\n".join([para.text for para in doc.paragraphs])


    def analyze_resume(resume_text, job_description):
        prompt = f"""
        You are an expert HR AI. Compare the following resume against the given job description.
        Evaluate the match percentage based on skills, experience, education, and relevant keywords.

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Output should strictly be:
        Candidate Name: <Name>
        Match Percentage: <Percentage>
        Email Id: <Email id>
        """

        response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
        return response.text


    def send_email(candidate_name, email_id, match_percentage):
        try:

            if match_percentage < 60:
                return  

            msg = EmailMessage()
            msg["Subject"] = "Congratulations! You've Been Shortlisted for an Interview"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = email_id

            msg.set_content(f"""
            Dear {candidate_name},

            Congratulations!  Your resume has been shortlisted for the interview process.
            Your match percentage for the applied job role is {match_percentage}%.


            Our HR team will contact you soon with further interview details.

            Best regards,  
            HR Team,
            Neuronix
            """)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  
                server.send_message(msg)  

            st.warning(f"Interview selection email sent to {email_id}")
        

        except Exception as e:
            st.error(f" Failed to send email: {e}")

        



    def generate_pdf(df):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(150, height - 40, "Shortlisted Candidates Report")

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(30, height - 80, "Rank")
        pdf.drawString(100, height - 80, "Candidate")
        pdf.drawString(250, height - 80, "Match Percentage")
        pdf.drawString(400, height - 80, "Email ID")

        pdf.setFont("Helvetica", 12)
        y_position = height - 100
        for index, row in df.iterrows():
            pdf.drawString(30, y_position, str(index))  
            pdf.drawString(100, y_position, row["Candidate"])  
            pdf.drawString(250, y_position, f"{row['Match Percentage']}%")  
            pdf.drawString(400, y_position, row["Email ID"]) 
            y_position -= 20

        pdf.save()
        buffer.seek(0)
        return buffer







    st.title("Resume Screener AI")

    job_description = st.text_area("Enter the Job Description", "")

    uploaded_files = st.file_uploader(
        "Upload multiple resumes (PDF/DOCX)",
        accept_multiple_files=True,
        type=["pdf", "docx"],
    )

    if job_description and uploaded_files:
        all_results = []
        shortlisted_results = []

        for file in uploaded_files:
            
            if file.type == "application/pdf":
                resume_text = extract_text_from_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(file)
            else:
                st.error("Unsupported file format!")
                continue

            analysis = analyze_resume(resume_text, job_description)

            match = re.search(
                r"Candidate Name:\s*(.+)\nMatch Percentage:\s*(\d+)%\nEmail Id:\s*(.+)", analysis
            )

            if match:
                candidate_name = match.group(1)
                match_percentage = int(match.group(2))
                email_id = match.group(3)

                all_results.append(
                    {
                        "Candidate": candidate_name,
                        "Match Percentage": match_percentage,
                        "Email ID": email_id,
                    }
                )

                if match_percentage >= 60:
                    shortlisted_results.append(
                        {
                            "Candidate": candidate_name,
                            "Match Percentage": match_percentage,
                            "Email ID": email_id,
                        }
                    )

        if all_results:
            df_all = pd.DataFrame(all_results)
            df_all = df_all.sort_values(by="Match Percentage", ascending=False).reset_index(drop=True)
            df_all.index = df_all.index + 1 
            df_all.index.name = "Rank"
            st.subheader("All Candidates (Including Rejected)")
            st.table(df_all)

        if shortlisted_results:
            df_shortlisted = pd.DataFrame(shortlisted_results)
            df_shortlisted = df_shortlisted.sort_values(by="Match Percentage", ascending=False).reset_index(drop=True)
            df_shortlisted.index = df_shortlisted.index + 1  
            df_shortlisted.index.name = "Rank"

            pdf_buffer = generate_pdf(df_shortlisted)

            st.download_button(
                label="Download Shortlisted Report (PDF)",
                data=pdf_buffer,
                file_name="Shortlisted_Candidates_Report.pdf",
                mime="application/pdf",
            )

            for row in df_shortlisted.itertuples():
                threading.Thread(
                    target=send_email, 
                    args=(row.Candidate, row._3, row._2)
                ).start()
        else:
            st.warning("No candidates were shortlisted (Match < 60%).")


