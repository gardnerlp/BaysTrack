import streamlit as st
from utils.navbar import navbar  # Import your navbar function

def habitat_cleaning_log():
    # Ensure the navbar is always visible
    navbar()  # Add the navbar here

    # Check if the form was submitted and reset session state if necessary
    if 'form_submitted' in st.session_state and st.session_state.form_submitted:
        # Clear the session state values for the form inputs
        st.session_state["habitat_name"] = None  # Reset habitat_name to None
        st.session_state["cleaning_type"] = None  # Reset cleaning_type to None
        # Reset the flag to avoid continuous clearing
        st.session_state.form_submitted = False
        st.rerun()  # Refresh the page to clear the form

    st.title("Habitat Cleaning Log")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Habitat")
        habitat_name = st.selectbox("Select Habitat", ["Habitat 1", "Habitat 2", "Habitat 3", "Other"], key="habitat_name", index=None)
    
    with col2:
        st.subheader("Select Cleaning Type")
        cleaning_type = st.selectbox("Select Cleaning Type", ["Deep Clean", "Routine Clean", "Spot Clean"], key="cleaning_type", index=None)
    
    if st.button("Submit Habitat Cleaning Log"):
        st.success("Habitat cleaning log submitted successfully!")
        
        # Set the flag to trigger the form clearing logic
        st.session_state.form_submitted = True

if __name__ == "__main__":
    habitat_cleaning_log()
