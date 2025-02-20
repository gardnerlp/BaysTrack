import streamlit as st
from Login import login_page

def navbar():
    # Sidebar navigation
    username = st.session_state["username"]

    st.sidebar.markdown(f"<p style='font-size:25px; font-weight:bold; font-family:'Calibri';'>{username}</p>",unsafe_allow_html=True)
    st.sidebar.page_link('app.py', label='Home')
    st.sidebar.page_link('pages/Notes.py', label='Notes')
    st.sidebar.page_link('pages/Calendar.py', label='Calendar')
    st.sidebar.page_link('pages/Ethogram_Form.py', label='Ethogram Form')
    if "role" in st.session_state and st.session_state["role"] == "admin":
        st.sidebar.page_link('pages/Admin.py', label='Admin')
        st.sidebar.page_link('pages/Habitat.py', label='Animal & Habitat')
    else:
        st.sidebar.page_link('pages/Admin.py', label='User')
    
    #st.sidebar.button("Logout", on_click=logout)
