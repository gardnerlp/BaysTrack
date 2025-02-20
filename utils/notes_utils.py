from database.postgresql_connection import init_postgres_connection

def get_notes(user_id):
    """
    Fetch all notes from the Notes table.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    SELECT 
        note_id, 
        (SELECT INITCAP(username) FROM Users b WHERE b.user_id = a.user_id) AS username,
        INITCAP(Title) AS Title, 
        content, 
        (SELECT name FROM categories c WHERE c.category_id = CAST(a.category AS INTEGER)) AS category,
        is_shared, 
        created_at, 
        updated_at, 
        is_pinned
    FROM Notes a
    where user_id=%s;
    """
    cursor.execute(query,user_id)
    notes = cursor.fetchall()
    conn.close()
    return notes

def get_notes_app(user_id):
    """
    Fetch all notes from the Notes table.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
        SELECT n1.*, '' as shared FROM Notes n1 where is_pinned = True and user_id=%s
        union all
        SELECT n2.*, '(SHARED NOTE)' as shared FROM Notes n2 where is_pinned = True and is_shared = true and user_id <> %s
    """
    cursor.execute(query, (user_id, user_id))
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_note(note_id):
    """
    Delete a note from the database using its note_id.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Notes WHERE note_id = %s", (note_id,))
    conn.commit()
    conn.close()


def add_note(user_id, title, content, category=None, is_shared=False):
    """
    Add a new note to the Notes table, optionally with a category.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()

    # Ensure the category is added to the Categories table
    category_id = None
    if category:
        category_id = add_category(category)

    query = """
        INSERT INTO Notes (user_id, title, content, category, is_shared, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        RETURNING note_id
    """
    cursor.execute(query, (user_id, title, content, category_id, is_shared))
    note_id = cursor.fetchone()[0]  # Retrieve the last inserted ID
    conn.commit()
    conn.close()
    return note_id

def search_notes(query, user_id, category=None, tag=None):
    conn = init_postgres_connection()
    cursor = conn.cursor()

    query_string = """
        SELECT 
            note_id, 
            (SELECT INITCAP(username) FROM Users b WHERE b.user_id = a.user_id) AS username,
            INITCAP(Title) AS Title, 
            content, 
            (SELECT name FROM categories c WHERE c.category_id = CAST(a.category AS INTEGER)) AS category,
            is_shared, 
            created_at, 
            updated_at, 
            is_pinned
    FROM Notes a WHERE user_id=%s and
        (title ILIKE %s OR content ILIKE %s)
    """
    params = [user_id, f'%{query}%', f'%{query}%']

    if category:
        query_string += " AND category = %s"
        params.append(category)
    if tag:
        query_string += " AND note_id IN (SELECT note_id FROM Note_Tags WHERE tag_id = %s)"
        params.append(tag)

    cursor.execute(query_string, params)
    notes = cursor.fetchall()
    conn.close()
    return notes

def pin_note(note_id, pin_status):
    """
    Update the pin status of the note.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Notes SET is_pinned = %s WHERE note_id = %s", (pin_status, note_id))
    conn.commit()
    conn.close()

def add_category(category_name):
    """
    Ensure the category exists in the Categories table and return its ID.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()

    # Check if the category already exists
    cursor.execute("SELECT category_id FROM Categories WHERE name = %s", (category_name,))
    existing_category = cursor.fetchone()

    if existing_category:
        return existing_category[0]  # Return the existing category ID

    # Insert the new category
    cursor.execute("INSERT INTO Categories (name) VALUES (%s) RETURNING category_id", (category_name,))
    category_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return category_id

def add_tag(note_id, tag_name):
    """
    Add a tag to a note, ensuring the tag exists in the Tags table.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()

    # Check if the tag already exists
    cursor.execute("SELECT id FROM Tags WHERE tag_name = %s", (tag_name,))
    existing_tag = cursor.fetchone()

    if not existing_tag:
        # Insert the new tag
        cursor.execute("INSERT INTO Tags (note_id, tag_name) VALUES (%s, %s) RETURNING id", (note_id, tag_name))
        tag_id = cursor.fetchone()[0]
    else:
        tag_id = existing_tag[0]

    # Insert into the Note_Tags table
    cursor.execute("INSERT INTO Note_Tags (note_id, tag_id) VALUES (%s, %s)", (note_id, tag_id))
    conn.commit()
    conn.close()
    return tag_id

def get_events():
    """
    Fetch all events from the Events table.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    conn.close()
    return events

def add_event(user_id, title, description, start_time, end_time, is_recurring=False, recurrence_pattern=None):
    """
    Add a new event to the Events table.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Events (user_id, title, description, start_time, end_time, is_recurring, recurrence_pattern, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """
    cursor.execute(query, (user_id, title, description, start_time, end_time, is_recurring, recurrence_pattern))
    conn.commit()
    conn.close()
