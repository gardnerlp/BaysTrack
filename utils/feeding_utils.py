import psycopg2
from psycopg2 import sql

# Function to insert feeding log data into PostgreSQL
def submit_feeding_log(feeding_type, name, food_type, amount_fed, leftover_food, deer_feed_scoops, notes):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",  # Replace with your PostgreSQL host
            database="Bays_Mountain",  # Replace with your PostgreSQL database name
            user="gardnerlp",  # Replace with your PostgreSQL username
            password="0418"  # Replace with your PostgreSQL password
        )
        cursor = conn.cursor()

        # Insert into the single feeding_log table
        query = sql.SQL("""
            INSERT INTO feeding_log (
                feeding_type, name, food_type, amount_fed, leftover_food, deer_feed_scoops, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)

        values = (
            feeding_type,  # "Individual" or "Group"
            name,
            food_type,
            amount_fed,
            leftover_food if leftover_food else None,  # Handle optional leftover_food
            deer_feed_scoops if deer_feed_scoops else None,  # Handle optional deer_feed_scoops
            notes
        )

        # Execute the query with the values
        cursor.execute(query, values)

        # Commit the transaction to save the data
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
