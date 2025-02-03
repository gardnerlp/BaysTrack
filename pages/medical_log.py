import streamlit as st
from utils.medical_utils import submit_medical_log
from utils.navbar import navbar

def medical_log_page():
    st.title("Medical Log")
    navbar()
    
    # Animal name and encounter type
    animal_name = st.text_input("Animal Name:", key="animal_name")
    encounter_type = st.selectbox("Encounter Type:", ["", "Routine Check", "Emergency", "Follow-up"], key="encounter_type")
    
    st.write("---")
    
    # Injuries Section
    with st.expander("Injuries"):
        injury_type = st.selectbox("Type:", ["", "Fracture", "Laceration", "Bruising"], key="injury_type")
        injury_description = st.text_area("Description:", key="injury_description")
        exam_type = st.selectbox("Exam Type:", ["", "X-ray", "Ultrasound", "Physical"], key="exam_type")
        sedated = st.radio("Sedated?", ["Yes", "No"], key="sedated_injury")
        vet_notified = st.radio("Vet Notified?", ["Yes", "No"], key="vet_notified_injury")
        vet_response = ""
        if vet_notified == "Yes":
            vet_response = st.text_area("Vet Response:", key="vet_response_injury")
        medication_administered = st.selectbox("Medication Administered:", ["", "Antibiotic", "Painkiller"], key="med_admin_injury")
        dosage = st.selectbox("Dosage:", ["", "Low", "Medium", "High"], key="dosage_injury")
        
        if st.button("Submit Injuries Data", key="submit_injury"):
            submit_medical_log(animal_name, encounter_type, "Injuries", {
                "injury_type": injury_type,
                "injury_description": injury_description,
                "exam_type": exam_type,
                "sedated": sedated,
                "vet_notified": vet_notified,
                "vet_response": vet_response,
                "medication_administered": medication_administered,
                "dosage": dosage,
            })
            st.experimental_rerun()
    
    st.write("---")
    
    # Sedation Section
    with st.expander("Sedation"):
        sedation_medication = st.selectbox("Medication Used:", ["", "Ketamine", "Diazepam"], key="sedation_med")
        sedation_kit = st.selectbox("Kit Used:", ["", "Kit A", "Kit B"], key="sedation_kit")
        administration_method = st.selectbox("Administration Method:", ["", "Injection", "Oral"], key="admin_method_sedation")
        dose = st.selectbox("Dose:", ["", "Low", "Medium", "High"], key="dose_sedation")
        time_administered = st.time_input("Time Administered:", key="time_admin_sedation")
        time_responded = st.time_input("Time Responded:", key="time_resp_sedation")
        
        if st.button("Submit Sedation Data", key="submit_sedation"):
            submit_medical_log(animal_name, encounter_type, "Sedation", {
                "sedation_medication": sedation_medication,
                "sedation_kit": sedation_kit,
                "administration_method": administration_method,
                "dose": dose,
                "time_administered": str(time_administered),
                "time_responded": str(time_responded),
            })
            st.experimental_rerun()
    
    st.write("---")
    
    # Medication Section
    with st.expander("Medication"):
        med_type = st.selectbox("Type:", ["", "Antibiotic", "Painkiller"], key="med_type")
        med_dose = st.selectbox("Dose:", ["", "Low", "Medium", "High"], key="med_dose")
        admin_route = st.selectbox("Administration Route:", ["", "Oral", "Injection"], key="admin_route")
        animal_accepted = st.radio("Animal Accepted?", ["Yes", "No"], key="animal_accepted")
        sedated_med = st.radio("Sedated?", ["Yes", "No"], key="sedated_med")
        
        if st.button("Submit Medication Data", key="submit_medication"):
            submit_medical_log(animal_name, encounter_type, "Medication", {
                "med_type": med_type,
                "med_dose": med_dose,
                "admin_route": admin_route,
                "animal_accepted": animal_accepted,
                "sedated": sedated_med,
            })
            st.experimental_rerun()
    
    st.write("---")
    
    # Vet Section
    with st.expander("Vet"):
        vet_type = st.selectbox("Type:", ["", "Consultation", "Surgery", "Follow-up"], key="vet_type")
        vet_name = st.text_input("Vet Name:", key="vet_name")
        frequency = st.text_input("Frequency:", key="frequency_vet")
        location = st.text_input("Location:", key="location_vet")
        
        if st.button("Submit Vet Data", key="submit_vet"):
            submit_medical_log(animal_name, encounter_type, "Vet", {
                "vet_type": vet_type,
                "vet_name": vet_name,
                "frequency": frequency,
                "location": location,
            })
            st.experimental_rerun()
    
if __name__ == "__main__":
    medical_log_page()
