from database.postgresql_connection import init_postgres_connection

def add_feedinglog(user_id, datetime, animal_group, individual_name, food_type, amount_fed, observation_type, leftover_food, deer_feed_scoops, meds_added, individual_notes, med_log_id,
                   nb_amount_fed, chicken_amount_fed, prey_amount_fed, fruits_amount_fed, veg_amount_fed, fish_amount_fed, mazuri_amount_fed, total_food_quantity):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO feeding_logs (user_id, datetime, animal_group, individual_name, food_type, amount_fed, observation_type, 
    leftover_food, deer_feed_scoops, meds_added, individual_notes, med_log_id,
    Nebraska, Chicken, WholePrey, Fruits, Vegetables, Fish, Mazuri, total_food_quantity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (user_id, datetime, animal_group, individual_name, food_type, amount_fed, observation_type, leftover_food, deer_feed_scoops, meds_added, individual_notes, med_log_id,
              nb_amount_fed, chicken_amount_fed, prey_amount_fed, fruits_amount_fed, veg_amount_fed, fish_amount_fed, mazuri_amount_fed, total_food_quantity)
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def add_medslog(user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO med_log (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (user_id, datetime, animal_group, individual_name, encounter_type, med_type, dose, administration_route, meds_taken)
    cursor.execute(query, params)
    med_log_id = cursor.fetchone()[0] 
    conn.commit()
    conn.close()
    return med_log_id

