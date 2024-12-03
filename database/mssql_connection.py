import pyodbc
from datetime import datetime

def init_mssql_connection():
    """
    Initializes a connection to the SQL Server using Windows Authentication.
    """
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LEND-2KVC6F3\\SQLEXPRESS;'
            'DATABASE=Bays_Mountain;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        raise


def get_user_details():
    """
    Fetch all user details from the Users table.
    """
    conn = init_mssql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return users


