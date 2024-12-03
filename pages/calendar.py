import streamlit as st
from utils.calendar_utils import add_task, update_task, get_tasks_by_date
from datetime import date

def calendar_page():
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

    for task in tasks:
        st.write(f"**{task.title}** - {task.description}")
