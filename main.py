import streamlit as st
import login_signup_page
import landing_main

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_email = None

if st.session_state.authenticated:
    landing_main.main()
else:
    login_signup_page.main()
