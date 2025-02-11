import psycopg2
from psycopg2 import sql

# Function to insert medical log data into PostgreSQL
def submit_medical_log(animal_name, encounter_type, log_type, log_data):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",  # Replace with your PostgreSQL host
            database="Bays_Mountain",  # Replace with your PostgreSQL database name
            user="gardnerlp",  # Replace with your PostgreSQL username
            password="0418"  # Replace with your PostgreSQL password
        )
        cursor = conn.cursor()

        # Prepare the insert query based on the log type
        if log_type == "Injuries":
            query = sql.SQL("""
                INSERT INTO medical_injuries (
                    animal_name, encounter_type, injury_type, injury_description, 
                    exam_type, sedated, vet_notified, vet_response, 
                    medication_administered, dosage
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)

            values = (
                animal_name, encounter_type, 
                log_data["injury_type"], log_data["injury_description"], 
                log_data["exam_type"], log_data["sedated"], 
                log_data["vet_notified"], log_data["vet_response"], 
                log_data["medication_administered"], log_data["dosage"]
            )
        
        elif log_type == "Sedation":
            query = sql.SQL("""
                INSERT INTO medical_sedation (
                    animal_name, encounter_type, sedation_medication, sedation_kit, 
                    administration_method, dose, time_administered, time_responded
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """)

            values = (
                animal_name, encounter_type, 
                log_data["sedation_medication"], log_data["sedation_kit"], 
                log_data["administration_method"], log_data["dose"], 
                log_data["time_administered"], log_data["time_responded"]
            )

        elif log_type == "Medication":
            query = sql.SQL("""
                INSERT INTO medical_medication (
                    animal_name, encounter_type, med_type, med_dose, 
                    admin_route, animal_accepted, sedated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)

            values = (
                animal_name, encounter_type, 
                log_data["med_type"], log_data["med_dose"], 
                log_data["admin_route"], log_data["animal_accepted"], 
                log_data["sedated"]
            )

        elif log_type == "Vet":
            query = sql.SQL("""
                INSERT INTO medical_vet (
                    animal_name, encounter_type, vet_type, vet_name, 
                    frequency, location
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """)

            values = (
                animal_name, encounter_type, 
                log_data["vet_type"], log_data["vet_name"], 
                log_data["frequency"], log_data["location"]
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
