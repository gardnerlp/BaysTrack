from database.mssql_connection import init_mssql_connection

def get_notes():
    """
    Fetch all notes from the Notes table.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Notes")
    notes = cursor.fetchall()
    conn.close()
    return notes


def add_note(user_id, title, content, category=None, is_shared=False):
    """
    Add a new note to the Notes table, optionally with a category.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    
    # Ensure the category is added to the Categories table
    category_id = None
    if category:
        category_id = add_category(category)

    query = """
        INSERT INTO Notes (user_id, title, content, category_id, is_shared, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
    """
    cursor.execute(query, (user_id, title, content, category_id, int(is_shared)))
    conn.commit()

    # Retrieve the last inserted ID
    cursor.execute("SELECT @@IDENTITY AS note_id")
    note_id = cursor.fetchone()[0]
    conn.close()
    return note_id


def search_notes(query, category=None, tag=None, is_pinned=None):
    conn = init_mssql_connection()
    cursor = conn.cursor()
    query_string = """
        SELECT * FROM Notes WHERE 
        (title LIKE ? OR content LIKE ?)
    """
    params = ['%' + query + '%', '%' + query + '%']

    if category:
        query_string += " AND category = ?"
        params.append(category)
    if tag:
        query_string += " AND id IN (SELECT note_id FROM NoteTags WHERE tag_id = ?)"
        params.append(tag)
    if is_pinned is not None:
        query_string += " AND is_pinned = ?"
        params.append(int(is_pinned))
    
    cursor.execute(query_string, params)
    notes = cursor.fetchall()
    conn.close()
    return notes


def pin_note(note_id, pin_status):
    # Update the pin status of the note
    conn = init_mssql_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Notes SET is_pinned = ? WHERE id = ?", (pin_status, note_id))
    conn.commit()


def add_category(category_name):
    conn = init_mssql_connection()
    cursor = conn.cursor()

    # Check if the category already exists
    cursor.execute("SELECT category_id FROM Categories WHERE name = ?", (category_name,))
    existing_category = cursor.fetchone()

    if existing_category:
        return existing_category[0]  # Return the existing category ID

    # Insert the new category
    cursor.execute("INSERT INTO Categories (name) VALUES (?)", (category_name,))
    conn.commit()

    # Return the new category ID
    cursor.execute("SELECT @@IDENTITY AS category_id")
    new_category_id = cursor.fetchone()[0]

    return new_category_id


def add_tag(tag_name):
    conn = init_mssql_connection()
    cursor = conn.cursor()

    # Check if the tag already exists
    cursor.execute("SELECT tag_id FROM Tags WHERE name = ?", (tag_name,))
    existing_tag = cursor.fetchone()

    if existing_tag:
        return existing_tag[0]  # Return the existing tag ID

    # Insert the new tag
    cursor.execute("INSERT INTO Tags (name) VALUES (?)", (tag_name,))
    conn.commit()

    # Return the new tag ID
    cursor.execute("SELECT @@IDENTITY AS tag_id")
    new_tag_id = cursor.fetchone()[0]

    return new_tag_id


def get_events():
    """
    Fetch all events from the Events table.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    conn.close()
    return events


def add_event(user_id, title, description, start_time, end_time, is_recurring=False, recurrence_pattern=None):
    """
    Add a new event to the Events table.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Events (user_id, title, description, start_time, end_time, is_recurring, recurrence_pattern, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())
    """
    cursor.execute(query, (user_id, title, description, start_time, end_time, int(is_recurring), recurrence_pattern))
    conn.commit()
    conn.close()
