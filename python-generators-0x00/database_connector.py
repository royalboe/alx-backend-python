import mysql.connector as connector
from mysql.connector import Error

class DB_connection:
  def __init__(self, db_name, user, password, host='localhost', port=3306):
    self.db_name = db_name
    self.user = user
    self.password = password
    self.host = host
    self.port = port

  def __enter__(self):
    print(f"Connecting to database {self.db_name} at {self.host}:{self.port} as user {self.user}")
    try:
      self.connection = connector.connect(
        host=self.host,
        port=self.port,
        user=self.user,
        password=self.password,
        database=self.db_name
      )
      if self.connection.is_connected():
        print("Connection established successfully.")
        return self.connection.cursor()
    except Error as e:
      print(f"Error while connecting to MySQL: {e}")
      raise

  # Ensure the connection is closed properly
  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.connection and self.connection.is_connected():
      self.connection.commit()
      self.connection.close()
      print(f"Connection to {self.db_name} closed successfully.")
      return True  # Suppress exceptions
    else:
      print("Connection was not open.")
      return False  # Do not suppress exceptions
    
user = 'prodev'
password = 'password123'
host = 'localhost'
db_name = 'ALX_prodev'

with DB_connection(db_name, user, password) as cursor:
  cursor.execute("SELECT DATABASE()")
  result = cursor.fetchone()
  print(result)
