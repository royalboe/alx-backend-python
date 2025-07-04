import mysql.connector as connector
from mysql.connector import errorcode, Error
# To use a generator ro compute a 
# memory-efficient aggregate function
# i.e average age for a large datatset

config = {
    'user': 'prodev',
    'password': 'password123',
    'host': 'localhost',
    'database': 'ALX_prodev'
}

def connect_db():
    """Connect to the MySQL engine and return the connection object."""
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

def stream_users_ages():
    """Generator function to fetch user ages from the user_data table."""
    connection = connect_db()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row['age']

    cursor.close()
    connection.close()

def average_age():
    """Calculate the average age of users using a generator."""
    total_age = 0
    count = 0

    for age in stream_users_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0
    avr_age = total_age / count
    print(f"Average age of users: {avr_age:.2f}")
    return avr_age


if __name__ == "__main__":
    import sys

    try:
        avg_age = average_age()
        print(f"Average age of users: {avg_age:.2f}")
    except BrokenPipeError:
        sys.stderr.write("Error: Broken pipe encountered.\n")
        sys.stderr.close()
    except OSError:
        sys.stderr.write("Error: Broken pipe or OSError encountered.\n")
        sys.stderr.close()

