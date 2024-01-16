import psycopg2
from psycopg2 import sql

# AWS RDS PostgreSQL connection details
db_host = "postgres1.citeitdsrarx.eu-central-1.rds.amazonaws.com"
db_port = "5432"
db_name = "postgres"
db_user = "postgres"
db_password = "Pa$$w0rd"

# SQL file to execute
sql_file_path = "./all.sql"


def execute_sql_script(connection, cursor, sql_file_path):
    with open(sql_file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script
    cursor.execute(sql_script)
    connection.commit()


try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    print("we got a connection")

    # Create a cursor object
    cursor = connection.cursor()

    # Execute SQL script
    execute_sql_script(connection, cursor, sql_file_path)

    print("SQL script executed successfully.")

except psycopg2.Error as e:
    print("Error connecting to the PostgreSQL database:", e)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
