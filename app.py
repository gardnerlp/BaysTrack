import streamlit as st
from utils.notes_utils import get_notes_app
from utils.calendar_utils import get_all_reminders
from Login import login_page
from utils.navbar import navbar

# Set page configuration early
st.set_page_config(initial_sidebar_state="collapsed")

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Default to not logged in
    
    if not st.session_state.logged_in:
        login_page()
    else:
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        else:
            # Extract query parameters for navigation
            query_params = st.query_params                    # experimental_get_query_params (Removed this because its outdated)
            page = query_params.get("page", ["main"])[0]

            if page == "notes":
                dashboard()
            else:
                dashboard()


def dashboard():
    """
    Main dashboard showing notes.
    """
    navbar()

    user_id = st.session_state["user_id"]

    st.title("Bays Mountain Dashboard")
    
    # Wrap the notes content inside the white-bordered container
    col1, col2 = st.columns([1, 1])
    with col1: 
        st.header("Notes")
        with st.container(height=300, border=True):
            notes = get_notes_app(str(user_id))
            if notes:
                for note in notes:
                    st.markdown(f"<p style='font-size:12.5px;'>{note[2]} - {note[3]} {note[9]}</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            else:
                st.write("No notes available.")

    with col2: 
        
        col1, col2 = st.columns([1, 0.7])
        with col1:
            st.header("Reminders")
        with col2:
            st.markdown(
                """ 
                <style>
                div[role="radiogroup"] {
                    margin-top: -15px;  /* Adjust this value to move it higher */
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            filter_option = st.radio("", ("All", "Self"), horizontal=True)
        with st.container(height=300, border=True):
            if filter_option == "All":
                var = ''
                reminders = get_all_reminders(var)
            else:
                reminders = get_all_reminders(str(user_id))
            if reminders:
                for reminder in reminders:
                    st.markdown(
                        f"<p style='font-size:12.5px;'>{reminder[1]}&nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;"
                        f"{reminder[4].capitalize()} : {reminder[2]} (Priority: {reminder[5]})</p>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            else:
                st.write("No reminders available.")


    with st.sidebar:
        if st.button("Logout", key="logout_button"):
            #del st.session_state["user_id"]
            #del st.session_state["username"]
            st.session_state.logged_in = False
            st.rerun()
            

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


def notes_page():
    """
    Displays the Notes page.
    """
    st.title("Notes Section")
    notes = get_notes_app()
    if notes:
        for note in notes:
            st.subheader(note[2])  # Assuming title is the third column
            st.write(note[3])  # Assuming content is the fourth column
    else:
        st.write("No notes available.")

if __name__ == "__main__":
    main()
