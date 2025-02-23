import streamlit as st
from Login import login_page
from utils.navbar import navbar

def main():
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

        # Log Type Selection Page
        st.title("Log Type")
        st.write("Select the type of log you want to record:")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Mammal Keeper Log")
            with st.container(border=True):
                if st.button("Feeding Log", use_container_width=True):
                    st.switch_page("pages/feeding_log.py")

                if st.button("Enrichment Log", use_container_width=True):
                    st.switch_page("pages/enrichment_log.py")

                if st.button("Habitat Cleaning Log", use_container_width=True):
                    st.switch_page("pages/habitat_cleaning_log.py")

                if st.button("Medical Log", use_container_width=True):
                    st.switch_page("pages/medical_log.py")

if __name__ == "__main__":
    main()
