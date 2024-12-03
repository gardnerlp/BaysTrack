from database.mssql_connection import init_mssql_connection

def add_task(title, description, date, assigned_to=None, is_reminder=False):
    """
    Add a new task to the Tasks table.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO Tasks (title, description, date, assigned_to, is_reminder, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
    """
    cursor.execute(query, (title, description, date, assigned_to, int(is_reminder)))
    conn.commit()
    conn.close()

def update_task(task_id, title=None, description=None, date=None, assigned_to=None, is_reminder=None):
    """
    Update an existing task in the Tasks table.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    updates = []
    params = []
    
    if title:
        updates.append("title = ?")
        params.append(title)
    if description:
        updates.append("description = ?")
        params.append(description)
    if date:
        updates.append("date = ?")
        params.append(date)
    if assigned_to is not None:
        updates.append("assigned_to = ?")
        params.append(assigned_to)
    if is_reminder is not None:
        updates.append("is_reminder = ?")
        params.append(int(is_reminder))
    
    query = f"UPDATE Tasks SET {', '.join(updates)}, updated_at = GETDATE() WHERE task_id = ?"
    params.append(task_id)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_tasks_by_date(date):
    """
    Retrieve all tasks for a specific date.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Tasks WHERE date = ?"
    cursor.execute(query, (date,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_all_tasks():
    """
    Retrieve all tasks for displaying on the main page.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Tasks ORDER BY date"
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    return tasks
