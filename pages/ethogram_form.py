import streamlit as st
from datetime import datetime

def ethogram_form():
    # Title of the form
    st.title("Ethogram Data Entry")

    # Behavior Type (dropdown or select box)
    behavior_type = st.selectbox("Select Behavior Type", ["Feeding", "Sleeping", "Socializing", "Other"])

    # Time of the behavior event (start time)
    event_time = st.time_input("Time of Behavior", value=datetime.now().time())

    # Duration of the behavior
    duration = st.number_input("Duration (in seconds)", min_value=0, step=1)

    # Notes/Additional Comments
    notes = st.text_area("Additional Comments/Notes")

    # Observer Information
    observer = st.text_input("Observer's Name")

    # Category/Tags for Classification (optional)
    category = st.text_input("Category/Tag (e.g., Feeding, Grooming)")

    # Submit button to save the data
    if st.button("Submit Data"):
        # Here you would handle saving the data, for now we'll just show a success message
        if observer and behavior_type and duration > 0:
            st.success(f"Data submitted successfully for {behavior_type}!")
            st.write(f"Time: {event_time}")
            st.write(f"Duration: {duration} seconds")
            st.write(f"Observer: {observer}")
            st.write(f"Category: {category}")
            st.write(f"Additional Notes: {notes}")
        else:
            st.error("Please fill in all fields before submitting.")

if __name__ == "__main__":
    ethogram_form()
