import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import resume_ranker
import analyze_my_resume
import resume_builder

def main():


    
    def logout():
        st.session_state.authenticated = False  
        st.session_state.user_email = None  
        st.session_state.user_role = None  
        st.session_state.user_name = None  
        st.session_state.logout_trigger = True  


    if "logout_trigger" in st.session_state and st.session_state.logout_trigger:
        st.success("Logged out successfully! Redirecting to login page...")
        st.session_state.logout_trigger = False  
        st.rerun()





    
    st.set_page_config(page_title="Resume Screener")

    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("Please log in first.")
        return


    

    
    user_role = st.session_state.get("user_role", "Candidate")
    user_name = st.session_state.get("user_name", "User") 
    email_id = st.session_state.get("user_email", "Email Id") 


    if user_role == "HR":
        st.sidebar.title(f" {user_name}")
        st.sidebar.text(f" {email_id}")
        st.sidebar.button("Logout", key="logout_hr", on_click=logout) 

        st.subheader(f"Welcome, {user_name}!")  
        resume_ranker.main()
        

    elif user_role == "Candidate":
        st.sidebar.title(f" {user_name}")
        st.sidebar.text(f" {email_id}")
        st.subheader(f"Welcome, {user_name}!")
        page = st.sidebar.radio("Go to", ["Analyze My Resume", "Resume Builder"])

        if page == "Analyze My Resume":
            analyze_my_resume.main()

        elif page == "Resume Builder":
            resume_builder.main()


        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False  
            st.session_state.user_email = None  
            st.session_state.user_role = None  

            st.success("Logged out successfully! Redirecting to login page...")
            st.rerun() 
