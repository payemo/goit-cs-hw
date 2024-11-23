import psycopg2
from psycopg2 import sql

CHECK_DATABASE_EXISTS = """
    SELECT 1 FROM pg_database WHERE datname=%s;
"""

CREATE_DATABASE_SQL = """
    CREATE DATABASE {};
"""

CREATE_USER_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
"""

CREATE_STATUS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
"""

CREATE_TASKS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER REFERENCES status(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
"""
 
INSERT_INITIAL_STATUS_SQL = """
    INSERT INTO status (name) VALUES
    ('new'),
    ('in progress'),
    ('completed')
    ON CONFLICT (name) DO NOTHING;
"""

# Database connection
DB_NAME = "task_manager"
DB_USER = "postgres"
DB_PASSWORD = "123"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    connection = psycopg2.connect(
        dbname = "postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    connection.autocommit = True
    cursor = connection.cursor()

    # Check if database exists
    cursor.execute(CHECK_DATABASE_EXISTS, [DB_NAME])
    exists = cursor.fetchone()

    # If database does not exist then create one
    if not exists:
        cursor.execute(sql.SQL(CREATE_DATABASE_SQL).format(sql.Identifier(DB_NAME)))
        print(f"Database '{DB_NAME}' was successfully created.")
    else:
        print(f"'{DB_NAME}' - OK.")
        
except Exception as e:
    print(f"Error during database creation: {e}")
finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()

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

    # Create user table
    cursor.execute(CREATE_USER_TABLE_SQL)
    
    # Create status table
    cursor.execute(CREATE_STATUS_TABLE_SQL)
    # Fill initial values for status
    cursor.execute(INSERT_INITIAL_STATUS_SQL)
    # Create task table

    cursor.execute(CREATE_TASKS_TABLE_SQL)

    print("Tables are created successfully.\n")
except Exception as e:
    print("Error during tables creation: {e}")
finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()