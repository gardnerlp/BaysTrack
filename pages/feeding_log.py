import streamlit as st
from Login import login_page
from utils.navbar import navbar
from streamlit_free_text_select import st_free_text_select
import uuid
from utils.feeding_utils import add_feedinglog, add_medslog
from datetime import datetime

def feeding_log():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Default to not logged in
    
    if not st.session_state.logged_in:
        login_page()
    else:
        navbar()

        with st.sidebar:
            if st.button("Logout", key="logout_button"):                
                st.session_state.logged_in = False
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.write(
                    """
                    <meta http-equiv="refresh" content="0; url=/" />
                    """,
                    unsafe_allow_html=True
                )
                st.stop()

        user_id = st.session_state["user_id"]
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if 'filter_option' not in st.session_state:
            st.session_state.filter_option = "Individual"
    
        # Check if the form was submitted and reset session state if necessary
        if 'form_submitted' in st.session_state and st.session_state.form_submitted:
            # Clear session state values for the form inputs only when the form is submitted
            st.session_state["individual_name"] = ""
            st.session_state["leftover_food"] = ""
            st.session_state["individual_notes"] = ""

            st.session_state.animal_key = get_unique_key("animal_select")
            st.session_state.food_key = get_unique_key("food_select")
            st.session_state.amount_key = get_unique_key("amount_select")

            #st.session_state.group_key = get_unique_key("group_select")
            #st.session_state.group_food_key = get_unique_key("group_food_select")
            #st.session_state.group_amount_key = get_unique_key("group_amount_select")

            st.session_state.observation_key = get_unique_key("observation_select")

            st.session_state["group_notes"] = ""
            if "deer_feed_scoops" in st.session_state:
                st.session_state["deer_feed_scoops"] = None
            
            st.session_state["meds_added"] = None
            st.session_state["med_type"] = ""
            st.session_state["dose"] = ""
            
            # Reset the form submission flag to prevent continuous resetting
            st.session_state.form_submitted = False
            st.rerun()  # Refresh the page to clear the form

        if st.button("Back", use_container_width=False):
            st.switch_page("pages/ethogram_form.py")
        
        col1, col2 = st.columns([1, 0.5])

        with col1:
            st.title("Feeding Log")

        with col2:
            filter_option = st.radio("Feeding Type", ["Individual", "Group"], horizontal=True, index=["Individual", "Group"].index(st.session_state.filter_option))
 
        with st.container(border=True): 
            if filter_option == "Individual":
                st.subheader("Individual Feedings")
            else:
                st.subheader("Group Feedings")
            
            if "animal_key" not in st.session_state:
                st.session_state.animal_key = "animal_select"
            if "food_key" not in st.session_state:
                st.session_state.food_key = "food_select"
            if "amount_key" not in st.session_state:
                st.session_state.amount_key = "amount_select"
            if "observation_key" not in st.session_state:    
                st.session_state.observation_key = "observation_select"
            
            animal_group = st_free_text_select(label="Animal Type *", options=["Bobcat","Deer","Red Fox","River Otter","Wolf"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter an animal",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.animal_key,
            )
            
            if filter_option == "Individual":
                individual_name = st.text_input("Enter Animal Name *", key="individual_name")
            else:
                individual_name = "All"
            
            food_type = st_free_text_select(label="Select Food Type *", options=["Chicken", "Whole Prey", "Fruits", "Fresh Vegetables"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter a food",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.food_key,
            )
            
            amount_fed = st_free_text_select(label="Select Amount Fed *", options=["0.25lb","0.5lb","0.75lb","1lb","1.25lb","1.5lb","1.75lb","2lb","5lb","10lb","15lb","20lb"],
                index=None,
                format_func=lambda x: x.lower(),
                placeholder="Select or enter the amount fed",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.amount_key,
            )

            observation_type = st_free_text_select(label="Select Observation Type *", options=["DVE","DPE"],
                index=None,
                format_func=lambda x: x.upper(),
                placeholder="Select or enter the observation",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.observation_key,
            )
            
            leftover_food = st.text_input("Enter Leftover Food", key="leftover_food")   
            
            if leftover_food == "": leftover_food = "0lb"

            if animal_group == "Deer":
                deer_feed_scoops = st.number_input("Enter Number of Deer Feed Scoops", min_value=0, step=1, key="deer_feed_scoops", value=None)
            else:
                deer_feed_scoops = 0

            meds_added = st.selectbox("Medication Added to Food", ["Yes", "No"], key="meds_added", index=None)
            
            if meds_added == "Yes":
                med_type = st.text_input("Enter Medication Type *", key="med_type")
                dose = st.text_input("Enter Medication Dosage *", key="dose")
                encounter_type = "Feeding"
                administration_type = "Oral"
            else:
                meds_added = "No"
                encounter_type = None
                med_type = None
                dose = None
                administration_type = None

            individual_notes = st.text_area("Notes", key="individual_notes")

            med_log_id = 0

            submitted = st.button("Submit Individual Feeding")                
            
            if submitted:
                if filter_option == "Individual" and not individual_name:
                    st.error("Please fill out the name of the Animal.")
                    return

                if not animal_group:
                    st.error("Please fill out Animal Type before submitting the feeding log.")
                    return
                if not food_type:
                    st.error("Please fill out Food Type before submitting the feeding log.")
                    return
                if not amount_fed:
                    st.error("Please fill out Amount Fed before submitting the feeding log.")
                    return
                if not observation_type:
                    st.error("Please fill out Observation Type before submitting the feeding log.")
                    return

                if meds_added == "Yes":
                    if not med_type:  
                        st.error("Please fill out the medication.")
                        return
                    if not dose:  # Ensure both fields are filled
                        st.error("Please fill out the dosage.")
                        return

                    # Add medication log
                    med_log_id = add_medslog(
                        user_id, 
                        formatted_time, 
                        animal_group, 
                        individual_name, 
                        encounter_type, 
                        med_type, 
                        dose, 
                        administration_type, 
                        meds_taken=True
                    )

                # Add feeding log (med_log_id is None if no meds were added)
                add_feedinglog(
                    user_id, 
                    formatted_time, 
                    animal_group, 
                    individual_name, 
                    food_type, 
                    amount_fed, 
                    observation_type, 
                    leftover_food, 
                    deer_feed_scoops, 
                    meds_added, 
                    individual_notes,
                    med_log_id
                )

                st.success("Individual feeding log submitted successfully!")
                st.session_state.filter_option = filter_option
                st.session_state.form_submitted = True
                st.rerun()
            

def get_unique_key(base_key):
        return f"{base_key}_{uuid.uuid4().hex[:6]}"
          
if __name__ == "__main__":
    feeding_log()