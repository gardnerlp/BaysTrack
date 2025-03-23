from database.postgresql_connection import init_postgres_connection

def add_habitat_cleaning_log(user_id, datetime, animal_group, observation_type, habitat, findings, desc_of_cleaning, pad_cleaning, water_change, pond_cleaning, waste_removal, brush_removal, fence_maintenance):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO habitat_log (user_id, datetime, animal_group, observation_type, habitat, findings, desc_of_cleaning, Pad_cleaning, Water_change, Pond_cleaning, Waste_removal, Brush_removal, Fence_maintenance)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, observation_type, habitat, findings, desc_of_cleaning, pad_cleaning, water_change, pond_cleaning, waste_removal, brush_removal, fence_maintenance)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

