import streamlit as st
from datetime import datetime
from database.mssql_connection import get_notes, add_note, search_notes, add_category, add_tag, pin_note
from streamlit_quill import st_quill

def notes_page():
    st.title("Collaborative Notes")
    
    # Section for searching notes
    st.subheader("Search Notes")
    search_query = st.text_input("Search notes by title or content:")

    # Display notes based on search query
    notes = search_notes(search_query) if search_query else get_notes()
    
    # Display notes with user and timestamp
    st.subheader("Your Notes")
    if notes:
        for note in notes:
            note_id, title, content, is_shared, created_at, user_id, is_pinned, category = (
                note[0],
                note[1],
                note[2],
                note[3],
                note[4],
                note[5],
                note[6],
                note[7],
            )

            with st.expander(f"{title} (Pinned: {'Yes' if is_pinned else 'No'})"):
                st.markdown(f"""
                **Category**: {category if category else "Uncategorized"}  
                **Content**: {content}  
                **Shared**: {"Yes" if is_shared else "No"}  
                **Created by**: {user_id}  
                **Created at**: {created_at.strftime('%Y-%m-%d %H:%M:%S')}
                """)
                if not is_pinned:
                    if st.button(f"Pin Note", key=f"pin_{note_id}"):
                        pin_note(note_id, True)
                        st.experimental_rerun()
                else:
                    if st.button(f"Unpin Note", key=f"unpin_{note_id}"):
                        pin_note(note_id, False)
                        st.experimental_rerun()
                st.write("---")
    else:
        st.info("No notes available. Add a new note to get started!")

    # Section to add a new note
    st.subheader("Add a New Note")
    user_id = st.text_input("Your Username:")
    title = st.text_input("Note Title:")
    category = st.text_input("Category (e.g., Work, Personal):")
    
    # Rich text editor for note content
    new_note = st_quill(label="Note Content:")
    is_shared = st.checkbox("Share this note with others?", value=False)
    
    # Add tags functionality
    tags_input = st.text_input("Add tags (comma-separated):")
    tags = tags_input.split(",") if tags_input else []

    if st.button("Add Note"):
        if not user_id or not title or not new_note:
            st.error("Please fill out all fields before adding the note.")
        else:
            # Add the note to the database
            note_id = add_note(user_id, title, new_note, category, is_shared)
            
            # Add tags to the database
            for tag in tags:
                add_tag(note_id, tag.strip())

            st.success("Note added successfully!")
            st.experimental_rerun()  # Refresh the page to show updated notes

