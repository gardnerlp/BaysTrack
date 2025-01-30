import streamlit as st
from Login import login_page
from utils.navbar import navbar
from datetime import datetime

def main():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Default to not logged in
    
    if not st.session_state.logged_in:
        login_page()
    else:
        if "user_id" in st.session_state:
            user_id = st.session_state["user_id"]
            username = st.session_state["username"]

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
        """
        Main function to manage navigation and render pages.
        """
        # Initialize session state for navigation
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'log_type'

        # Handle navigation
        if st.session_state.current_page == 'log_type':
            log_type_page()
        elif st.session_state.current_page == 'feeding_log':
            feeding_log_page()
        elif st.session_state.current_page == 'enrichment_log':
            enrichment_log_page()
        elif st.session_state.current_page == 'habitat_cleaning_log':
            habitat_cleaning_log_page()
        elif st.session_state.current_page == 'medical_log':
            medical_log_page()

def log_type_page():
    """
    Page displaying log type buttons.
    """
    st.title("Log Type")

    st.write("Select the type of log you want to record:")

    if st.button("Feeding Log"):
        st.session_state.current_page = 'feeding_log'
    if st.button("Enrichment Log"):
        st.session_state.current_page = 'enrichment_log'
    if st.button("Habitat Cleaning Log"):
        st.session_state.current_page = 'habitat_cleaning_log'
    if st.button("Medical Log"):
        st.session_state.current_page = 'medical_log'

def feeding_log_page():
    """
    Page for feeding log data entry.
    """
    st.title("Feeding Log")

    if st.button("← Back"):
        st.session_state.current_page = 'log_type'

    with st.form('Feeding Form',clear_on_submit=True):
        behavior_type = st.selectbox("Select Feeding Type", ["Herbivore", "Carnivore", "Omnivore"])
        event_time = st.time_input("Time of Feeding", value=datetime.now().time())
        duration = st.number_input("Duration (in seconds)", min_value=0, step=1)
        observer = st.text_input("Observer's Name")
        notes = st.text_area("Additional Comments/Notes")
        submitted = st.form_submit_button("Submit Data")

        if submitted:
            if observer and duration > 0:
                st.success("Feeding log submitted successfully!")
                st.write(f"Feeding Type: {behavior_type}")
                st.write(f"Time: {event_time}")
                st.write(f"Duration: {duration} seconds")
                st.write(f"Observer: {observer}")
                st.write(f"Notes: {notes}")
            else:
                st.error("Please fill in all fields before submitting.")

def enrichment_log_page():
    """
    Page for enrichment log data entry.
    """
    st.title("Enrichment Log")

    if st.button("← Back"):
        st.session_state.current_page = 'log_type'

    with st.form('Enrichment Form',clear_on_submit=True):
        enrichment_type = st.selectbox("Select Enrichment Type", ["Physical", "Mental", "Sensory"])
        event_time = st.time_input("Time of Enrichment", value=datetime.now().time())
        duration = st.number_input("Duration (in seconds)", min_value=0, step=1)
        observer = st.text_input("Observer's Name")
        notes = st.text_area("Additional Comments/Notes")
        submitted = st.form_submit_button("Submit Data")

        if submitted:
            if observer and duration > 0:
                st.success("Enrichment log submitted successfully!")
                st.write(f"Enrichment Type: {enrichment_type}")
                st.write(f"Time: {event_time}")
                st.write(f"Duration: {duration} seconds")
                st.write(f"Observer: {observer}")
                st.write(f"Notes: {notes}")
            else:
                st.error("Please fill in all fields before submitting.")

def habitat_cleaning_log_page():
    """
    Page for habitat cleaning log data entry.
    """
    st.title("Habitat Cleaning Log")

    if st.button("← Back"):
        st.session_state.current_page = 'log_type'

    with st.form('Habitat Form',clear_on_submit=True):
        cleaning_area = st.selectbox("Select Area to Clean", ["Cage", "Outdoor Habitat", "Aquarium"])
        event_time = st.time_input("Time of Cleaning", value=datetime.now().time())
        duration = st.number_input("Duration (in minutes)", min_value=0, step=1)
        observer = st.text_input("Observer's Name")
        notes = st.text_area("Additional Comments/Notes")
        submitted = st.form_submit_button("Submit Data")

        if submitted:
            if observer and duration > 0:
                st.success("Habitat cleaning log submitted successfully!")
                st.write(f"Cleaning Area: {cleaning_area}")
                st.write(f"Time: {event_time}")
                st.write(f"Duration: {duration} minutes")
                st.write(f"Observer: {observer}")
                st.write(f"Notes: {notes}")
            else:
                st.error("Please fill in all fields before submitting.")

def medical_log_page():
    """
    Page for medical log data entry.
    """
    st.title("Medical Log")

    if st.button("← Back"):
        st.session_state.current_page = 'log_type'

    with st.form('Medical Form',clear_on_submit=True):
        medical_procedure = st.selectbox("Select Procedure Type", ["Check-up", "Vaccination", "Treatment"])
        event_time = st.time_input("Time of Procedure", value=datetime.now().time())
        observer = st.text_input("Observer's Name")
        notes = st.text_area("Additional Comments/Notes")
        submitted = st.form_submit_button("Submit Data")

        if submitted:
            if observer:
                st.success("Medical log submitted successfully!")
                st.write(f"Procedure Type: {medical_procedure}")
                st.write(f"Time: {event_time}")
                st.write(f"Observer: {observer}")
                st.write(f"Notes: {notes}")
            else:
                st.error("Please fill in all fields before submitting.")

if __name__ == "__main__":
    main()
