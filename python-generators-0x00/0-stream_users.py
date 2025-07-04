
import mysql.connector as connector
from mysql.connector import errorcode, Error

def connect_to_prodev():
  """ Connect to the ALX_prodev database and return the connection object."""
  try:
    cnx = connector.connect(
      user='prodev', 
      password='password123',
      host='localhost',
      database='ALX_prodev'
    )
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

def stream_users():
  """ Generator function to fetch rows one by one from the user_data table."""
  connection = connect_to_prodev()
  if not connection:
    return

  cursor = connection.cursor(dictionary=True)
  cursor.execute("SELECT * FROM user_data")

  while True:
    row = cursor.fetchone()
    if row is None:
      break
    yield row

  cursor.close()
  connection.close()

if __name__ == "__main__":
  from itertools import islice

  # iterate over the generator function and print only the first 6 rows

  for user in islice(stream_users(), 6):
      print(user)