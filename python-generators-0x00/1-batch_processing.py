import mysql.connector as connector
from mysql.connector import errorcode, Error

config = {
  'user': 'prodev',
  'password': 'password123',
  'host': 'localhost',
  'database': 'ALX_prodev'
}

def connect_db():
  """Connect to database and return the connection object."""
  try:
    cnx = connector.connect(**config)

    if cnx.is_connected():
      return cnx
  except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Wrong username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  return None
  

def stream_users_in_batches(batch_size):
  """Generator function to fetch rows in batches from the user_data table."""
  connection = connect_db()
  if not connection:
    return None

  cursor = connection.cursor(dictionary=True)
  cursor.execute("SELECT * FROM user_data")

  while True:
    rows = cursor.fetchmany(batch_size)
    if not rows:
      break
    yield rows

  cursor.close()
  connection.close()

def batch_processing(batch_size):
  """Process users in batches and print them."""
  for batch in stream_users_in_batches(batch_size):
    batch = [user for user in batch if user['age'] >= 25]  # Filter users with age >= 25
    for user in batch:
      print(user)

if __name__ == "__main__":
  import sys

  ##### print processed users in a batch of 50
  try:
    batch_processing(50)
  except BrokenPipeError:
    # Handle BrokenPipeError for Unix-like systems
    sys.stderr.write("Error: Broken pipe encountered.\n")
    sys.stderr.close()
  except OSError:
    # OSError is equivalent of BrokenPipeError for windows
    sys.stderr.write("Error: Broken pipe or OSError encountered.\n")
    sys.stderr.close()