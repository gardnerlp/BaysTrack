import streamlit as st
from Login import login_page
from utils.navbar import navbar  # Import your navbar function
from streamlit_free_text_select import st_free_text_select
import uuid
from utils.habitat_cleaning_utils import add_habitat_cleaning_log
from datetime import datetime

def habitat_cleaning_log():
    
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

        # Check if the form was submitted and reset session state if necessary
        if 'form_submitted' in st.session_state and st.session_state.form_submitted:
            
            st.session_state["habitat_name"] = None
            st.session_state["cleaning_type"] = None
            st.session_state["individual_notes"] = ""
            st.session_state["findings"] = ""
            st.session_state.animal_key = get_unique_key("animal_select")
            st.session_state.observation_key = get_unique_key("observation_select")
            st.session_state.habitat_key = get_unique_key("habitat_select")
            
            st.session_state.form_submitted = False
            st.rerun() 

        
        if st.button("Back", use_container_width=False):
            st.switch_page("pages/ethogram_form.py")
        
        st.title("Habitat Cleaning Log")
        
        
        with st.container(border=True):
            
            if "animal_key" not in st.session_state:
                st.session_state.animal_key = "animal_select"
            if "observation_key" not in st.session_state:    
                st.session_state.observation_key = "observation_select"
            if "habitat_key" not in st.session_state:    
                st.session_state.habitat_key = "habitat_select"
            
            animal_group = st_free_text_select(
                label="Animal Type",
                options=["Bobcat", "Deer", "Red Fox", "River Otter", "Wolf"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter an animal",
                disabled=False,
                delay=300,
                key=st.session_state.animal_key, 
                label_visibility="visible",
            )

            observation_type = st_free_text_select(label="Select Observation Type", options=["DVE","DPE"],
                index=None,
                format_func=lambda x: x.upper(),
                placeholder="Select or enter the observation",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.observation_key,
            )
            
            habitat_name = st_free_text_select(label="Select Habitat", options=["Habitat 1", "Habitat 2", "Habitat 3"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter the Habitat",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.habitat_key,
            )
            
            #cleaning_type = st.selectbox("Select Cleaning Type", ["Deep Clean", "Routine Clean", "Spot Clean"], key="cleaning_type", index=None)

            findings = st.text_input("Findings", key="findings") #if findings == "": findings = "NSF"
            description = st.text_area("Description of Cleaning", key="individual_notes")
        
            if st.button("Submit Habitat Cleaning Log"):
                if not animal_group:
                    st.error("Please fill out Animal Type before submitting the habitat log.")
                    return
                if not observation_type:
                    st.error("Please select or enter Observation Type before submitting the habitat log.")
                    return
                if not habitat_name:
                    st.error("Please select or enter Habitat Name before submitting the habitat log.")
                    return
                if not description:
                    st.error("Please enter Cleaning Description before submitting the habitat log.")
                    return
                
                add_habitat_cleaning_log(user_id, formatted_time, animal_group, observation_type, habitat_name, findings, description)

                st.success("Habitat cleaning log submitted successfully!")
                st.session_state.form_submitted = True
                st.rerun()

def get_unique_key(base_key):
        return f"{base_key}_{uuid.uuid4().hex[:6]}"

if __name__ == "__main__":
    habitat_cleaning_log()
