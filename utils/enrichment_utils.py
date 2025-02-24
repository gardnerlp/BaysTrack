from database.postgresql_connection import init_postgres_connection

def add_enrichment_log(user_id, datetime, animal_group, observation_type, individual_name, enrichment_type, enrichment_details, time_in, time_out):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO enrichment_log (user_id, datetime, animal_group, observation_type, individual_name, enrichment_type, enrichment_details, time_in, time_out)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, observation_type, individual_name, enrichment_type, enrichment_details, time_in, time_out)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

