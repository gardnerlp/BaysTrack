import streamlit as st
from datetime import datetime

def main():
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

    behavior_type = st.selectbox("Select Feeding Type", ["Herbivore", "Carnivore", "Omnivore"])
    event_time = st.time_input("Time of Feeding", value=datetime.now().time())
    duration = st.number_input("Duration (in seconds)", min_value=0, step=1)
    observer = st.text_input("Observer's Name")
    notes = st.text_area("Additional Comments/Notes")

    if st.button("Submit Data"):
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

    enrichment_type = st.selectbox("Select Enrichment Type", ["Physical", "Mental", "Sensory"])
    event_time = st.time_input("Time of Enrichment", value=datetime.now().time())
    duration = st.number_input("Duration (in seconds)", min_value=0, step=1)
    observer = st.text_input("Observer's Name")
    notes = st.text_area("Additional Comments/Notes")

    if st.button("Submit Data"):
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

    cleaning_area = st.selectbox("Select Area to Clean", ["Cage", "Outdoor Habitat", "Aquarium"])
    event_time = st.time_input("Time of Cleaning", value=datetime.now().time())
    duration = st.number_input("Duration (in minutes)", min_value=0, step=1)
    observer = st.text_input("Observer's Name")
    notes = st.text_area("Additional Comments/Notes")

    if st.button("Submit Data"):
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

    medical_procedure = st.selectbox("Select Procedure Type", ["Check-up", "Vaccination", "Treatment"])
    event_time = st.time_input("Time of Procedure", value=datetime.now().time())
    observer = st.text_input("Observer's Name")
    notes = st.text_area("Additional Comments/Notes")

    if st.button("Submit Data"):
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
