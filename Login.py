import streamlit as st
from utils.user_utils import authenticate_user, get_user_details

def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        role = authenticate_user(email, password)
        user = get_user_details(email)
        if role:
            st.success("Login successful!")
            st.session_state["user_id"] = user[0][0]  # Assuming username[0] is user_id
            st.session_state["username"] = user[0][1]  # Assuming username[1] is username
            st.success(f"Welcome, {st.session_state['username']}!")
            st.session_state.logged_in = True
            st.session_state.role = role
            st.query_params = {"page": "main"}
            st.rerun()
        else:
            st.error("Invalid email or password.")
