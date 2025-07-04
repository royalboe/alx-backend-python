import mysql.connector as connector
from mysql.connector import errorcode, Error
import uuid
import csv


config = {
  'user':'prodev', 
  'password':'password123',
  'host':'localhost',
}
def connect_db():
  """Connect to the MySQL engine and return the connection object."""
  try:
    cnx = connector.connect(**config)
    if cnx.is_connected():
      print("Connection successful")
      # print("Connection successful", cnx.server_info)
      return cnx
  except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Wrong username or password")
    else:
      print(err)
      return None
  
def create_database(cnx):
  """Create the ALX_prodev database if it does not exist."""
  try:
    # A cursor is a control structure that lets you execute SQL commands and fetch results from the database connection
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    print("Database ALX_prodev is present.")
    # cursor.close()
  except Error as err:
    print(f'Error creating database: {err}')

def connect_to_prodev():
  """Connect to the ALX_prodev database."""
  try:
    config['database'] = 'ALX_prodev'  # Set the database to connect to
    cnx = connector.connect(**config)
    if cnx.is_connected():
      # print("Connected to ALX_prodev database.")
      return cnx
  except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Wrong username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
      return None
    
def create_table(cnx):
  """
    Create the users table in the ALX_prodev database.
    MYSQL doesn't support UUID, to use UUIDS, use char(36) or binary(16).
    Here, we use UUID as a string (char(36)).
  """
  try:
    create_table_query = """
      CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        age INT NOT NULL,
        INDEX idx_users_email (email),
        INDEX idx_users_user_id (user_id)
      )
    """
    cursor = cnx.cursor()
    cursor.execute(create_table_query)
    print("Table user_data created successfully.")
    cursor.close()
  except Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
      print("Table user_data already exists.")
    # Handle other errors
    if err.errno == errorcode.ER_BAD_FIELD_ERROR:
      print("Error: Bad field in the table definition.")
    elif err.errno == errorcode.ER_PARSE_ERROR:
      print("Error: Parse error in the SQL statement.")
    else:
      print(f'Error creating table: {err}')

def insert_data(connection, data):
  """Insert data into the users table."""
  try:
    cursor = connection.cursor()
    with open(data, mode='r', newline='', encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      data_to_insert = [
        (
          str(uuid.uuid4()),  # Generate a new UUID for user_id
          row['name'],
          row['email'],
          float(row['age'])
        )
        for row in reader
      ]
    if not data_to_insert:
      print("No data to insert.")
      return None
    
    insert_query = """
      INSERT INTO user_data (user_id, name, email, age)
      VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(insert_query, data_to_insert)
    connection.commit()
    print(f"{cursor.rowcount} rows inserted.")
    cursor.close()
  except Error as err:
    print(f'Error inserting data: {err}')
  except FileNotFoundError:
    print(f'File {data} not found.')
  except KeyError as e:
    print(f'Key error: {e}. Ensure the CSV file has the correct headers.')
  except ValueError as e:
    print(f'Value error: {e}. Ensure the data types in the CSV file are correct.')
  except Exception as e:
    print(f'An unexpected error occurred: {e}')


if __name__ == "__main__":
  connection = connect_db()
  if connection:
      create_database(connection)
      connection.close()
      print(f"connection successful")

      connection = connect_to_prodev()

      if connection:
          create_table(connection)
          insert_data(connection, 'user_data.csv')
          cursor = connection.cursor()
          cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
          result = cursor.fetchone()
          if result:
              print(f"Database ALX_prodev is present ")
          cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
          rows = cursor.fetchall()
          print(rows)
          cursor.close()
          connection.close()
