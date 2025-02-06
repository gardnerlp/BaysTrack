import psycopg2
from psycopg2 import sql

def init_postgres_connection():
    """
    Initializes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",  # Replace with your PostgreSQL host
            database="Bays_Mountain",  # Replace with your PostgreSQL database name
            user="gardnerlp",  # Replace with your PostgreSQL username
            password="0418"  # Replace with your PostgreSQL password
        )
        return conn
    except Exception as e:
        print("Error connecting to the PostgreSQL database:", e)
        raise

