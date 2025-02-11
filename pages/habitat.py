import streamlit as st
from utils.animal_utils import insert_animal, insert_animal_profile, insert_habitat, get_habitat, get_animal, get_animal_habitat
from Login import login_page
from utils.navbar import navbar
import time

def habitat_page():
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
                st.stop()

        st.title("Wildlife Database Entry")

        # Form to add Habitat
        st.markdown('<div id="add_habitat"></div>', unsafe_allow_html=True)
        st.header("Add Habitat")
        with st.form(key='habitat_form', clear_on_submit=True):
            habitat_name = st.text_input("Habitat Name")
            description = st.text_area("Description")
            location = st.text_input("Location")
            size = st.text_input("Size in acers")
            submit_habitat = st.form_submit_button(label='Add Habitat')
            if submit_habitat:
                if habitat_name and description and location and size:
                    insert_habitat(habitat_name, description, location, size)
                    msg = st.success("Habitat added successfully!")
                    time.sleep(2)
                    msg.empty()
                else:
                    msg = st.error("All fields are required.")
                    time.sleep(2)
                    msg.empty()

        # Form to add Animal
        st.markdown('<div id="add_animal"></div>', unsafe_allow_html=True)
        st.header("Add Animal")
        habitats = get_habitat()
        habitat_dict = {habitat[0]: f"{habitat[1]} ({habitat[2]})" for habitat in habitats}
        reverse_habitat_dict = {v: k for k, v in habitat_dict.items()}
        habitat_list = list(habitat_dict.values())

        with st.form(key='animal_form', clear_on_submit=True):
            habitat_info = st.selectbox("Habitat", options=habitat_list, index=None)
            habitat_id = reverse_habitat_dict.get(habitat_info)
            common_name = st.text_input("Common Name")
            scientific_name = st.text_input("Scientific Name")
            status = st.selectbox("Active Status", ["True", "False"], index=0)
            submit_animal = st.form_submit_button(label='Add Animal')
            if submit_animal:
                if habitat_id and common_name and scientific_name and status:
                    insert_animal(habitat_id, common_name, scientific_name, status)
                    msg = st.success("Animal added successfully!")
                    time.sleep(2)
                    msg.empty()
                else:
                    msg = st.error("All fields are required.")
                    time.sleep(2)
                    msg.empty()

        # Form to add Animal Profile
        st.markdown('<div id="add_profile"></div>', unsafe_allow_html=True)
        st.header("Add Animal Profile")
        animals = get_animal()
        animal_dict = {animal[0]: f"{animal[2]} -- (Habitat: {animal[1]})" for animal in animals}
        reverse_animals_dict = {v: k for k, v in animal_dict.items()}
        animal_list = list(animal_dict.values())

        with st.form(key='animal_profile_form', clear_on_submit=True):
            animal_info = st.selectbox("Animal", options=animal_list, index=None)
            animal_id = reverse_animals_dict.get(animal_info)
            name = st.text_input("Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Neutral"], index=0)
            diet = st.text_input("Diet")
            lifespan = st.text_input("Lifespan in years")
            behavior = st.text_area("Behavior")
            fun_fact = st.text_area("Fun Fact")
            submit_animal_profile = st.form_submit_button(label='Add Animal Profile')
            if submit_animal_profile:
                if animal_id and name and gender and diet and lifespan:
                    insert_animal_profile(animal_id, diet, lifespan, behavior, fun_fact, name, gender)
                    msg = st.success("Animal profile added successfully!")
                    time.sleep(2)
                    msg.empty()
                else:
                    msg = st.error("All fields are required.")
                    time.sleep(2)
                    msg.empty()

        #Button to navigate to add user section
        st.markdown("""
            <a href="#add_habitat">
                <button style="position: fixed; right: 20px; bottom: 450px; padding: 10px 20px; width: 168px; background-color: #4CAF50; color: white; border: none; border-radius: 25px; font-size: 16px; cursor: pointer;">
                    Add Habitat
                </button>
            </a>
        """, unsafe_allow_html=True)

        #Button to navigate to add user section
        st.markdown("""
            <a href="#add_animal">
                <button style="position: fixed; right: 20px; bottom: 400px; padding: 10px 20px; width: 168px; background-color: #4CAF50; color: white; border: none; border-radius: 25px; font-size: 16px; cursor: pointer;">
                    Add Animal Type
                </button>
            </a>
        """, unsafe_allow_html=True)

        #Button to navigate to add user section
        st.markdown("""
            <a href="#add_profile">
                <button style="position: fixed; right: 20px; bottom: 350px; padding: 10px 20px; width: 168px; background-color: #4CAF50; color: white; border: none; border-radius: 25px; font-size: 16px; cursor: pointer;">
                    Add Animal Profile
                </button>
            </a>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    habitat_page()