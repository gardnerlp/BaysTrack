import streamlit as st
import pandas as pd
from datetime import date
from utils.calendar_utils import get_users, add_reminder, get_reminders, update_reminder, delete_reminder  # Adjust for your actual DB methods
from Login import login_page
from utils.navbar import navbar

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
                
                # Inject custom CSS to collapse the sidebar -- Need to rework on this
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
                # Add st.stop to ensure no further code execution
                st.stop()
                

            # JavaScript injection for styling
            st.markdown(
                """
                <script>
                const logoutButton = document.querySelector('#logout_button');
                if (logoutButton) {
                    logoutButton.style.marginTop = 'auto'; // Push to bottom
                    logoutButton.style.marginBottom = '20px';
                    logoutButton.style.width = '100%';
                    logoutButton.style.position = 'absolute';
                    logoutButton.style.bottom = '0';
                    logoutButton.style.left = '0';
                }
                </script>
                """,
                unsafe_allow_html=True,
            )
    
            st.title("Calendar & Reminders")

            # Ensure user is logged in
            if "user_id" not in st.session_state:
                st.warning("Please log in to access the calendar.")
                return

            user_id = st.session_state["user_id"]

            # Fetch all users (for assigning reminders)
            users = get_users()  # Returns a list of all users as [(user_id, username, email)]
            user_dict = {user[0]: f"{user[1]} ({user[2]})" for user in users}  # user_id: "username (email)"
            user_list = list(user_dict.values())

            # Fetch reminders for the logged-in user
            reminders = get_reminders(user_id)
            
            # Display reminders
            st.subheader("Your Reminders")
            if reminders.empty:
                st.info("No reminders set.")
            else:
                for i, reminder in reminders.iterrows():
                    with st.expander(f"{reminder['title']} (Priority: {reminder['priority']})"):
                        st.write(f"**Date:** {reminder['date']}")
                        st.write(f"**Description:** {reminder['description']}")
                        st.write(f"**Assigned to:** {user_dict.get(reminder['assigned_to'], 'Self')}")
                        
                        # Edit and delete buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Edit", key=f"edit_{i}"):
                                edit_reminder(reminder, users)
                        with col2:
                            if st.button("Delete", key=f"delete_{i}"):
                                delete_reminder(reminder["id"])
                                st.success("Reminder deleted successfully!")
                                st.experimental_rerun()

            # Add Reminder Section
            st.header("Add a Reminder")
            reminder_date = st.date_input("Select Date", min_value=date.today())
            reminder_title = st.text_input("Reminder Title")
            reminder_description = st.text_area("Description")
            assigned_to = st.selectbox("Assign to User", options=["Self"] + user_list, index=0)
            priority = st.radio("Priority Level", options=["High", "Medium", "Low"], index=1)

            if st.button("Add Reminder"):
                if reminder_title.strip():
                    assigned_to_user_id = None if assigned_to == "Self" else [k for k, v in user_dict.items() if v == assigned_to][0]
                    add_reminder(
                        user_id=user_id,
                        date=reminder_date,
                        title=reminder_title,
                        description=reminder_description,
                        assigned_to=assigned_to_user_id,
                        priority=priority
                    )
                    st.success("Reminder added successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Title cannot be empty.")

def edit_reminder(reminder, users):
    """Edit an existing reminder."""
    st.subheader("Edit Reminder")
    reminder_date = st.date_input("Select Date", value=pd.to_datetime(reminder["date"]))
    reminder_title = st.text_input("Reminder Title", value=reminder["title"])
    reminder_description = st.text_area("Description", value=reminder["description"])

    # Assign to User
    user_dict = {user[0]: f"{user[1]} ({user[2]})" for user in users}
    user_list = list(user_dict.values())
    assigned_to = st.selectbox(
        "Assign to User",
        options=["Self"] + user_list,
        index=0 if reminder["assigned_to"] is None else user_list.index(user_dict[reminder["assigned_to"]])
    )

    # Priority Level
    priority = st.radio(
        "Priority Level",
        options=["High", "Medium", "Low"],
        index=["High", "Medium", "Low"].index(reminder["priority"])
    )

    if st.button("Save Changes"):
        assigned_to_user_id = None if assigned_to == "Self" else [k for k, v in user_dict.items() if v == assigned_to][0]
        update_reminder(
            reminder_id=reminder["id"],
            date=reminder_date,
            title=reminder_title,
            description=reminder_description,
            assigned_to=assigned_to_user_id,
            priority=priority
        )
        st.success("Reminder updated successfully!")
        st.experimental_rerun()

if __name__ == "__main__":
    calendar_page()