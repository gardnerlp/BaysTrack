from database.postgresql_connection import init_postgres_connection
from passlib.hash import bcrypt

def authenticate_user(email, password):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM Users WHERE active = True and LOWER(email) = LOWER(%s)", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.verify(password, user[0]):
        return user[1]  # Return the role if authentication is successful
    return None

# Hash a password
def hash_password(password):
    return bcrypt.hash(password)

# Verify a password
def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def add_user(username, email, hashed_password, role, active):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Users (username, email, password, role, created_at, active) VALUES (INITCAP(%s), LOWER(%s), %s, %s, NOW(), %s)",
        (username, email, hashed_password, role, active)
    )
    conn.commit()
    conn.close()

def get_user_details(email):
    conn = init_postgres_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, INITCAP(username) FROM Users WHERE LOWER(email) = LOWER(%s)", (email,))
        users = cursor.fetchall()
        return users
    except Exception as e:
        print("Error executing query:", e)
        raise
    finally:
        conn.close()

def check_email_exists(email):
    """
    Check if an email already exists in the database.
    """
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM Users WHERE LOWER(email) = LOWER(%s)"
    cursor.execute(query, (email,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def get_all_users():
    conn = init_postgres_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT user_id, INITCAP(username), email, role, active FROM Users
                       order by user_id
                       """)
        users = cursor.fetchall()
        return users
    except Exception as e:
        print("Error executing query:", e)
        raise
    finally:
        conn.close()

def get_users_det(user_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = "SELECT user_id, INITCAP(username), email, role, active FROM users WHERE user_id = %s"
    params = (user_id,)
    cursor.execute(query, params)
    user = cursor.fetchall() 
    conn.close()
    return user

def update_user(user_id, email, role, active):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET email = %s, role = %s, active = %s
        WHERE User_id = %s
    """, (email, role, active, user_id))
    conn.commit()
    conn.close()

def update_password(user_id, password):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET password = %s
        WHERE User_id = %s
    """, (password, user_id))
    conn.commit()
    conn.close()