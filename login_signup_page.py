import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests

if not firebase_admin._apps:
    cred = credentials.Certificate("airesume-cf9b8-a8bf8374b679.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()  

FIREBASE_WEB_API_KEY = "AIzaSyA3z-3qHKVeHcFfkCq7px1T7boWyzuK1gI"

def verify_password(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def main():

    st.set_page_config(page_title="Login / Signup")
    st.title("Welcome to Resume Screener")


    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_email = None  
        st.session_state.user_role = None  

    auth_option = st.selectbox("Choose an option", ["Login", "Sign Up"])

    if auth_option == "Sign Up":
        st.subheader("Create a New Account")

        name = st.text_input("Name", placeholder="Enter your Full Name")
        email = st.text_input("Email", placeholder="Enter your email")
        user_role = st.selectbox("User Role", ["HR", "Candidate"])  
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Re-enter your password", type="password")

        if st.button("Sign Up"):
            if password != confirm_password:
                st.error("Passwords do not match! Please try again.")
            elif not email or not password:
                st.warning("All fields are required!")
            else:
                try:
                    user = auth.create_user(email=email, password=password,)

                    db.collection("users").document(user.uid).set({  
                        "name" : name,
                        "email": email,
                        "role": user_role
                    })

                    st.success("Account created successfully!  You can now log in.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")

    elif auth_option == "Login":
        st.subheader("Login to Your Account")

        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        if st.button("Login"):
            if not email or not password:
                st.warning("Both fields are required!")
            else:
                auth_response = verify_password(email, password)

                if "idToken" in auth_response:  
                    user_id = auth_response.get("localId")

                    user_doc = db.collection("users").document(user_id).get()
                    if user_doc.exists:
                        user_data = user_doc.to_dict()  
                        user_role = user_data.get("role")
                        user_name = user_data.get("name")  
                        
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_role = user_role  
                        st.session_state.user_name = user_name  

                        st.success(f"Welcome back, {user_name}! (Role: {user_role}) Redirecting...")

                        st.rerun()  

                    else:
                        st.error("User role not found. Please contact support.")
                else:  
                    st.error("Invalid email or password. Please try again.")

