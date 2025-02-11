from database.postgresql_connection import init_postgres_connection

def insert_habitat(habitat_name, description, location, size):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Habitat (habitat_name, description, location, size) VALUES (%s, %s, %s, %s)",
        (habitat_name, description, location, size)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Function to insert data into Animals table
def insert_animal(habitat_id, common_name, scientific_name, status=True):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Animals (habitat_id, common_name, scientific_name, status) VALUES (%s, %s, %s, %s)",
        (habitat_id, common_name, scientific_name, status)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Function to insert data into AnimalProfile table
def insert_animal_profile(animal_id, diet, lifespan, behavior, fun_fact, name, gender):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO AnimalProfile (animal_id, diet, lifespan, behavior, fun_fact, name, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (animal_id, diet, lifespan, behavior, fun_fact, name, gender)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_habitat():
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT habitat_id, INITCAP(habitat_name), location, size FROM HABITAT")
    habitat = cursor.fetchall()
    conn.close()
    return habitat

def get_animal():
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT animal_id, (SELECT INITCAP(habitat_name) FROM HABITAT b where b.habitat_id = a.habitat_id) as habitat, 
                   INITCAP(common_name), Upper(scientific_name) FROM Animals a
                   """)
    habitat = cursor.fetchall()
    conn.close()
    return habitat

def get_animal_habitat(animal_id):
    conn = init_postgres_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT habitat_id FROM Animals where animal_id=%s",(animal_id))
    anihab = cursor.fetchone()
    conn.close()
    return anihab