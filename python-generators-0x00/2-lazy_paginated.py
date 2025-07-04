import mysql.connector as connector
from mysql.connector import errorcode, Error

# Database configuration
# Note: Ensure to replace 'prodev', 'password123', 'localhost', and 'ALX_prodev' with your actual database credentials.
# This configuration is used to connect to the MySQL database.
config = {
  'user':'prodev', 
  'password':'password123',
  'host':'localhost',
  'database':'ALX_prodev'
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

def paginate_users(page_size, offset=0):
  """Fetch users from the database with pagination."""
  cnx = connect_db()
  if not cnx:
    return []

  cursor = cnx.cursor(dictionary=True)
  query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
  
  try:
    cursor.execute(query, (page_size, offset))
    users = cursor.fetchall()
    return users
  except Error as err:
    print(f"Error: {err}")
    return []
  finally:
    cursor.close()
    cnx.close()

def lazy_paginated_users(page_size):
  """Generator to yield users in a paginated manner."""
  offset = 0
  while True:
    users = paginate_users(page_size, offset)
    if not users:
      break
    for user in users:
      yield user
    offset += page_size


if __name__ == "__main__":
  import sys
  try:
    for user in lazy_paginated_users(100):
      print(user)
  except BrokenPipeError:
    # Handle BrokenPipeError for Unix-like systems
    sys.stderr.write("Error: Broken pipe encountered.\n")
    sys.stderr.close()
  except OSError:
    # OSError is equivalent of BrokenPipeError for windows
    sys.stderr.write("Error: Broken pipe or OSError encountered.\n")
    sys.stderr.close()
# This script connects to a MySQL database, fetches users in a paginated manner,
# and yields each user one by one. The `lazy_paginated_users` function is a
# generator that allows for lazy loading of user data, which is useful for
# handling large datasets without loading everything into memory at once.