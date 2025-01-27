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
    try:
        cursor.execute("""
            UPDATE reminders
            SET date = %s, title = %s, description = %s, assigned_to = %s, priority = %s
            WHERE id = %s
        """, (date, title, description, assigned_to, priority, reminder_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating reminder: {e}")
        return False
    finally:
        conn.close()

def get_users():
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = "SELECT user_id, username, email FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    return users

def get_users_det(user_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = "SELECT user_id, username, email FROM users WHERE user_id = %s"
    params = (user_id)
    cursor.execute(query, params)
    user = cursor.fetchone() 
    conn.close()
    if user:
        return f"{user[1]} ({user[2]})"  # user[1] = username, user[2] = email
    else:
        return "User not found"

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

def get_all_reminders():
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    SELECT id, date, title, description, assigned_to, priority
    FROM reminders
    """
    cursor.execute(query)
    reminders_all = cursor.fetchall()
    conn.close()
    return reminders_all

def delete_reminder(reminder_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = %s", (reminder_id,))
    conn.commit()
    conn.close()

