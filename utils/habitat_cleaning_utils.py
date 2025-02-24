from database.postgresql_connection import init_postgres_connection

def add_habitat_cleaning_log(user_id, datetime, animal_group, observation_type, habitat, findings, desc_of_cleaning):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO habitat_log (user_id, datetime, animal_group, observation_type, habitat, findings, desc_of_cleaning)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, observation_type, habitat, findings, desc_of_cleaning)
    cursor.execute(query, params)
    conn.commit()
    conn.close()