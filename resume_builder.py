import streamlit as st
from fpdf import FPDF

def main():


    def generate_pdf(name, email, phone, summary, experience, education, skills, achievements):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, name, ln=True, align="C")
        
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Email: {email}", ln=True, align="C")  # Fix: Ensure email is displayed
        pdf.cell(200, 10, f"Phone: {phone}", ln=True, align="C")  # Fix: Move phone to a new line
        pdf.ln(10)
        
        sections = [
            ("Summary", summary),
            ("Experience", experience),
            ("Education", education),
            ("Skills", skills),
            ("Achievements", achievements)
        ]
        
        for title, content in sections:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(200, 10, title, ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(5)

        return pdf

    st.title("Resume Builder")

    name = st.text_input("Full Name")
    email = st.text_input("Email")  # Ensure this is entered
    phone = st.text_input("Phone Number")
    summary = st.text_area("Summary", placeholder="Write a brief summary about yourself...")
    experience = st.text_area("Work Experience", placeholder="Describe your past work experience...")
    education = st.text_area("Education", placeholder="List your educational background...")
    skills = st.text_area("Skills", placeholder="List your skills...")
    achievements = st.text_area("Achievements", placeholder="List your achievements...")

    if st.button("Generate PDF"):
        if not email.strip():  # Check if email is empty
            st.error("Please enter your email before generating the PDF.")
        else:
            pdf = generate_pdf(name, email, phone, summary, experience, education, skills, achievements)
            
            pdf_path = "resume.pdf"
            pdf.output(pdf_path)
            
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(label="Download Resume", data=pdf_file, file_name="resume.pdf", mime="application/pdf")

