import streamlit as st
import pandas as pd
from datetime import date
from utils.calendar_utils import get_users, add_reminder, get_reminders, update_reminder, delete_reminder, get_users_det  # Adjust for your actual DB methods
from Login import login_page
from utils.navbar import navbar
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
from streamlit_calendar import calendar

def calendar_page():
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

        url = st_javascript("await fetch('').then(r => window.parent.location.href)")
               
        st.title("Calendar & Reminders")

        # Ensure user is logged in
        if "user_id" not in st.session_state:
            st.warning("Please log in to access the calendar.")
            return

        user_id = st.session_state["user_id"]

        # Initialize editing state
        if "editing_reminder" not in st.session_state:
            st.session_state.editing_reminder = None

        # Fetch all users (for assigning reminders)
        users = get_users()  # Returns a list of all users as [(user_id, username, email)]
        user_dict = {user[0]: f"{user[1].upper()} ({user[2]})" for user in users}  # user_id: "username (email)"
        user_dict_name = {user[0]: user[1].upper() for user in users}  # user_id: "username "
        user_list = list(user_dict.values())

        # Fetch reminders for the logged-in user
        reminders = get_reminders(user_id)
        
        # Display reminders
        st.subheader("Your Reminders")
        with st.container(height=300, border=True):
            if not reminders:
                st.info("No reminders set.")
            else:
                for i, reminder in enumerate(reminders):
                    with st.expander(f"{reminder[1]}&nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;{user_dict_name.get(reminder[4], 'Unknown')} : {reminder[2]} (Priority: {reminder[5]})"):  # Indexes based on query order
                        st.write(f"Date: {reminder[1]}")
                        st.write(f"Description: {reminder[3]}")
                        st.write(f"Assigned To: {user_dict.get(reminder[4], 'Unknown')}")
                        
                        # Edit and delete buttons
                        col1, col2 = st.columns([5, 1]) 
                        with col1:
                            if st.button("Edit  ", key=f"edit_{i}"):
                                st.session_state.editing_reminder = {
                                    "id": reminder[0],
                                    "date": reminder[1],
                                    "title": reminder[2],
                                    "description": reminder[3],
                                    "assigned_to": reminder[4],
                                    "priority": reminder[5]
                                }
                                scroll(url,"add_Reminder")
                                st.rerun()
                        with col2:
                            if st.button("Delete", key=f"delete_{i}"):
                                delete_reminder(reminder[0])
                                st.success("Reminder deleted successfully!")
                                st.rerun()
        
        # Add/Update Reminder Section
        st.markdown('<div id="add_Reminder"></div>', unsafe_allow_html=True)
        st.header("Add a Reminder", anchor="add-reminder-section")
        reminder = st.session_state.editing_reminder
        with st.form('Notes Form', clear_on_submit=(reminder is None)):
            reminder_date = st.date_input(
                "Select Date", 
                value=reminder["date"] if reminder else date.today()
            )
            reminder_title = st.text_input(
                "Reminder Title", 
                value=reminder["title"] if reminder else ""
            )
            reminder_description = st.text_area(
                "Description", 
                value=reminder["description"] if reminder else ""
            )
            
            # Ensure the assigned_to index is valid
            if reminder and user_dict.get(reminder["assigned_to"], "Unknown") in user_list:
                assigned_to_index = user_list.index(user_dict.get(reminder["assigned_to"], "Unknown")) 
            else:
                assigned_to_index = 0
            
            assigned_to = st.selectbox(
                "Assign to User", 
                options= user_list,     #["Self"] +
                index=assigned_to_index
            )

            priority = st.radio(
                "Priority Level", 
                options=["High", "Medium", "Low"], 
                index=["High", "Medium", "Low"].index(reminder["priority"]) if reminder else 1
            )
            submitted = st.form_submit_button("Save Reminder")

            if submitted:
                if reminder_title.strip():
                    assigned_to_user_id = user_id if assigned_to == "Self" else [k for k, v in user_dict.items() if v == assigned_to][0]
                    if reminder:  # Update existing reminder
                        update_reminder(
                            reminder_id=reminder["id"],
                            date=reminder_date,
                            title=reminder_title,
                            description=reminder_description,
                            assigned_to=assigned_to_user_id,
                            priority=priority
                        )
                        st.success("Reminder updated successfully!")
                        st.session_state.editing_reminder = None
                    else:  # Add new reminder
                        add_reminder(
                            user_id=user_id,
                            date=reminder_date,
                            title=reminder_title,
                            description=reminder_description,
                            assigned_to=assigned_to_user_id,
                            priority=priority
                        )
                        st.success("Reminder added successfully!")
                    st.rerun()
                else:
                    st.error("Title cannot be empty.")

def scroll(html, element_id):
    return html.replace('</body>', """
    <script>
        window.onload = function() {{
            console.log("Attempting to scroll to element with ID: {}");
            var element = document.getElementById("{}");
            if (element) {{
                console.log("Element found, scrolling into view.");
                element.scrollIntoView();
            }} else {{
                console.log("Element not found.");
            }}
        }};
    </script>
    </body>
    """.format(element_id, element_id))

def scroll_test(html, element_id):
    return html.replace('</body>', """      
    <script>
        var element = document.getElementById("{}");
        element.scrollIntoView();
    </script>
    </body>
    """.format(element_id))     #.encode()

if __name__ == "__main__":
    calendar_page()
