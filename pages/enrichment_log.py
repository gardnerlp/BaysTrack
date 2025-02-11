import streamlit as st
from utils.navbar import navbar  # Import your navbar function

def enrichment_log():
    # Ensure the navbar is always visible
    navbar()  # Add the navbar here

    # Check if the form was submitted and reset session state if necessary
    if 'form_submitted' in st.session_state and st.session_state.form_submitted:
        # Clear the session state values for the form inputs
        st.session_state["individual_name"] = ""
        st.session_state["enrichment_type"] = None
        st.session_state["details"] = ""
        st.session_state["time_in"] = None
        st.session_state["time_out"] = None
        st.session_state["response"] = ""
        # Reset the flag to avoid continuous clearing
        st.session_state.form_submitted = False
        st.rerun()  # Refresh the page to clear the form

    st.title("Enrichment Log")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Individual Information")
        individual_name = st.text_input("Enter Individual's Name", key="individual_name")
        enrichment_type = st.selectbox("Select Enrichment Type", ["Toys", "Training", "Exploration", "Other"], key="enrichment_type", index=None)

    with col2:
        st.subheader("Details and Response")
        details = st.text_area("Enter Details of the Enrichment", key="details")
        
        # Time input for Time In (30-minute increments)
        time_in_options = [
            f"{hour:02}:{minute:02} AM" if hour < 12 else f"{hour-12:02}:{minute:02} PM"
            for hour in range(1, 13) for minute in [0, 30]
        ]
        time_in = st.selectbox("Select Time In", time_in_options, key="time_in", index=None)

        # Time input for Time Out (30-minute increments)
        time_out = st.selectbox("Select Time Out", time_in_options, key="time_out", index=None)

        response = st.text_area("Enter Response", key="response")

    if st.button("Submit Enrichment Log"):
        st.success("Enrichment log submitted successfully!")
        
        # Set the flag to trigger the form clearing logic
        st.session_state.form_submitted = True

if __name__ == "__main__":
    enrichment_log()
