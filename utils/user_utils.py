from database.postgresql_connection import init_postgres_connection
import bcrypt

def authenticate_user(email, password):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM Users WHERE LOWER(email) = LOWER(%s)", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        return user[1]  # Return the role if authentication is successful
    return None

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

# Verify a password
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password)


def add_user(username, email, hashed_password, role):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Users (username, email, password, role, created_at) VALUES (%s, LOWER(%s), %s, %s, NOW())",
        (username, email, hashed_password, role)
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