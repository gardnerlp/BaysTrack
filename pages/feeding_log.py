import streamlit as st
from utils.navbar import navbar

def feeding_log():
    navbar()
    # Check if the form was submitted and reset session state if necessary
    if 'form_submitted' in st.session_state and st.session_state.form_submitted:
        # Clear the session state values for the form inputs
        st.session_state["individual_name"] = ""
        st.session_state["food_type_individual"] = None  # Reset food_type to None
        st.session_state["amount_fed_individual"] = None  # Reset amount_fed to None
        st.session_state["leftover_food"] = ""
        st.session_state["individual_notes"] = ""
        st.session_state["group_name"] = None  # Reset group_name to None
        st.session_state["amount_fed_group"] = None  # Reset amount_fed_group to None
        st.session_state["group_notes"] = ""
        if "deer_feed_scoops" in st.session_state:
            st.session_state["deer_feed_scoops"] = None  # Reset deer_feed_scoops to None
        # Reset the flag to avoid continuous clearing
        st.session_state.form_submitted = False
        st.rerun()  # Refresh the page to clear the form

    st.title("Feeding Log")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Individual Feedings")
        individual_name = st.text_input("Enter Individual's Name", key="individual_name")
        food_type = st.selectbox("Select Food Type", ["Hay", "Pellets", "Fruits", "Vegetables", "Other"], key="food_type_individual", index=None)
        amount_fed = st.selectbox("Select Amount Fed", ["0.25lb", "0.5lb", "1lb", "2lb", "5lb", "10lb"], key="amount_fed_individual", index=None)
        leftover_food = st.text_input("Enter Leftover Food", key="leftover_food")
        individual_notes = st.text_area("Notes", key="individual_notes")
    
    with col2:
        st.subheader("Group Feedings")
        group_name = st.selectbox("Select Group", ["Deer", "Wolves", "Birds", "Other"], key="group_name", index=None)
        group_food_type = st.selectbox("Select Food Type", ["Hay", "Pellets", "Fruits", "Vegetables", "Other"], key="food_type_group", index=None)
        group_amount_fed = st.selectbox("Select Amount Fed", ["0.25lb", "0.5lb", "1lb", "2lb", "5lb", "10lb"], key="amount_fed_group", index=None)
        if group_name == "Deer":
            deer_feed_scoops = st.number_input("Enter Number of Deer Feed Scoops", min_value=0, step=1, key="deer_feed_scoops", value=None)
        else:
            deer_feed_scoops = None
        group_notes = st.text_area("Notes", key="group_notes")
    
    if st.button("Submit Feeding Log"):
        st.success("Feeding log submitted successfully!")
        
        # Set the flag to trigger the form clearing logic
        st.session_state.form_submitted = True
        st.rerun()

if __name__ == "__main__":
    feeding_log()
