from database.postgresql_connection import init_postgres_connection

def add_reminder(user_id, date, title, description, assigned_to=None, priority="Medium"):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO reminders (user_id, date, title, description, assigned_to, priority)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (user_id, date, title, description, assigned_to, priority)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def update_reminder(reminder_id, date, title, description, assigned_to, priority):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    UPDATE reminders
    SET date = %s, title = %s, description = %s, assigned_to = %s, priority = %s
    WHERE id = %s
    """
    params = (date, title, description, assigned_to, priority, reminder_id)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_users():
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = "SELECT user_id, username, email FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    return users

def get_reminders(user_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    SELECT id, date, title, description, assigned_to, priority
    FROM reminders
    WHERE user_id = %s OR assigned_to = %s
    """
    params = (user_id, user_id)
    cursor.execute(query, params)
    reminders = cursor.fetchall()
    conn.close()
    return reminders


