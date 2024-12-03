import streamlit as st
from utils.notes_utils import get_notes
from utils.calendar_utils import get_all_tasks, get_tasks_by_date, add_task
from datetime import date

def main():
    # Extract query parameters for navigation
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["main"])[0]

    if page == "notes":
        notes_page()
    elif page == "calendar":
        calendar_page()
    else:
        dashboard()

def dashboard():
    """
    Main dashboard showing notes and calendar tasks side by side.
    """
    st.title("Bays Mountain Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Notes")
        notes = get_notes()
        if notes:
            for note in notes:
                st.subheader(note.title)
                st.write(note.content)
        else:
            st.write("No notes available.")

    with col2:
        st.header("Tasks")
        tasks = get_all_tasks()
        if tasks:
            for task in tasks:
                st.subheader(task.title)
                st.write(f"Due Date: {task.date}")
                st.write(task.description)
        else:
            st.write("No tasks available.")

    st.sidebar.button("Go to Notes", on_click=lambda: st.experimental_set_query_params(page="notes"))
    st.sidebar.button("Go to Calendar", on_click=lambda: st.experimental_set_query_params(page="calendar"))

def notes_page():
    """
    Displays the Notes page.
    """
    st.title("Notes Section")
    st.write("This section will display detailed functionality for managing notes.")
    # Add existing note management logic here if needed.

def calendar_page():
    """
    Displays the Calendar page.
    """
    st.title("Calendar Management")

    with st.sidebar:
        st.subheader("Add a New Task")
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_date = st.date_input("Task Date", min_value=date.today())
        is_reminder = st.checkbox("Set as Reminder?")
        assigned_to = st.text_input("Assigned To (User ID, leave blank for none)")

        if st.button("Add Task"):
            add_task(task_title, task_description, task_date, assigned_to or None, is_reminder)
            st.success("Task added successfully!")

    st.subheader("Tasks by Date")
    selected_date = st.date_input("View Tasks For Date")
    tasks = get_tasks_by_date(selected_date)

    if tasks:
        for task in tasks:
            st.write(f"**{task.title}** - {task.description}")
            st.write(f"Assigned To: {task.assigned_to if task.assigned_to else 'No specific user'}")
            st.write("---")
    else:
        st.write("No tasks found for the selected date.")

if __name__ == "__main__":
    main()
