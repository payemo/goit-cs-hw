import psycopg2
from faker import Faker
import random

# Database connection
DB_NAME = "task_manager"
DB_USER = "postgres"
DB_PASSWORD = "123"
DB_HOST = "localhost"
DB_PORT = "5432"

NUM_USERS = 10
NUM_TASKS = 10

try:
    connection = psycopg2.connect(
        dbname = DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    connection.autocommit = True
    cursor = connection.cursor()

    faker = Faker()

    # Inserting random users
    for _ in range(NUM_USERS):
        fullname = faker.name()
        email = faker.unique.email()
        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)",
            (fullname, email)
        )
    print(f"{NUM_USERS} users have been successfully added.")

    # Get users id
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Get status
    cursor.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cursor.fetchall()]

    # Inserting random tasks
    for _ in range(NUM_TASKS):
        title = faker.sentence(nb_words=6)
        description = faker.text(max_nb_chars=100)
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)

        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES(%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )
    print(f"{NUM_USERS} tasks have been successfully created.")


except Exception as e:
    print(f"Error during seeding process: {e}")
finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()