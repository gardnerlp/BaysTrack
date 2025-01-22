import streamlit as st
from bcrypt import checkpw
from Login import login_page
from utils.user_utils import add_user, hash_password, check_email_exists
from utils.navbar import navbar

def admin_page():
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Default to not logged in
    
    if not st.session_state.logged_in:
        login_page()
    else:
        navbar()
        with st.sidebar:
            if st.button("Logout", key="logout_button"):                
                
                # Inject custom CSS to collapse the sidebar -- Need to rework on this
                hide_sidebar_css = """
                    <style>
                        [data-testid="stSidebar"] {
                            display: none;
                        }
                    </style>
                """
                st.markdown(hide_sidebar_css, unsafe_allow_html=True)

                st.session_state.logged_in = False
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.write(
                    f"""
                    <meta http-equiv="refresh" content="0; url=/" />
                    """,
                    unsafe_allow_html=True
                )
                # Add st.stop to ensure no further code execution
                st.stop()
                

            # JavaScript injection for styling
            st.markdown(
                """
                <script>
                const logoutButton = document.querySelector('#logout_button');
                if (logoutButton) {
                    logoutButton.style.marginTop = 'auto'; // Push to bottom
                    logoutButton.style.marginBottom = '20px';
                    logoutButton.style.width = '100%';
                    logoutButton.style.position = 'absolute';
                    logoutButton.style.bottom = '0';
                    logoutButton.style.left = '0';
                }
                </script>
                """,
                unsafe_allow_html=True,
            )
        
        if st.session_state.role != 'admin':
            st.error("You do not have access to this page.")
            return

        st.title("Admin Page")
        st.header("Add New User")

        # Form to add a new user
        with st.form('Admin From',clear_on_submit=True):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["user", "admin"])  # Allow admin to assign roles
            
            #add_user_button = st.button("Add User")
            submitted = st.form_submit_button("Add User")

            if submitted:
                if username and email and password:
                    if check_email_exists(email):
                        st.error("This email is already in use. Please use a different email.")
                    else:
                        hashed_password = hash_password(password).decode('utf-8')
                        add_user(username, email, hashed_password, role)
                        st.success(f"User {username} added successfully!")
                else:
                    st.error("All fields are required.")

if __name__ == "__main__":
    admin_page()