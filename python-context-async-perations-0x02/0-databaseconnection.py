import mysql.connector as connector
from mysql.connector import Error
from typing import Any

class DatabaseConnection:
    """
        Context manager for managing a MySQL database connection.

        Example usage:
            with DatabaseConnection('db_name', 'user', 'password') as cursor:
                cursor.execute("SELECT * FROM users;")
                rows = cursor.fetchall()
        """
    def __init__(self, db_name: str, db_user: str, db_password: str, db_port: int=3306, db_host: str='localhost') -> None:

        """
            Initialize the DatabaseConnection object with connection details.

            Args:
                db_name (str): Name of the database to connect to.
                db_user (str): Username for authentication.
                db_password (str): Password for authentication.
                db_port (int, optional): Port number for MySQL. Defaults to 3306.
                db_host (str, optional): Hostname or IP address. Defaults to 'localhost'.
        """

        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.db_host = db_host

        return

    def __enter__(self) -> connector.cursor.MySQLCursor:
        """
            Establish the database connection and return a cursor.

            Returns:
                MySQLCursor: Cursor object to execute queries.
        """
        print(f"Connecting to database {self.db_name} at {self.db_host}:{self.db_port} as user {self.db_user}")
        try:
            self.cnx = connector.connect(
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                port=self.db_port,
                host=self.db_host
            )
            if self.cnx.is_connected():
                print("Connection established successfully.")
                return self.cnx.cursor()
        except Error as e:
            print(f'Error connecting to Database {self.db_name} on {self.db_host}: {e}')
            raise

    def __exit__(self, exc_type: type|None, exc_value: BaseException|None, exc_traceback: Any|None) -> bool:
        """
            Commit changes and close the database connection.

            Args:
                exc_type (Optional[type]): Exception type if raised.
                exc_value (Optional[BaseException]): Exception value if raised.
                exc_traceback (Optional[Any]): Traceback object.

            Returns:
                bool: True if connection closed successfully, False otherwise.
        """

        if self.cnx and self.cnx.is_connected():
            self.cnx.commit()
            self.cnx.close()
            print(f"Connection to {self.db_name} closed successfully.")
            return True
        else:
            print("Connection was not open.")
            return False  # Do not suppress exceptions

user = 'prodev'
password = 'password123'
host = 'localhost'
database = 'ALX_prodev'


def populate_db(cur: connector.cursor.MySQLCursor) -> None:
    """
    Creates the users table if it does not exist and populates it only if empty.

    Args:
        cur: MySQL cursor object to execute queries.
    """
    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT,
            email VARCHAR(150) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    cur.execute(create_table_query)
    # Check if table already has data
    cur.execute("SELECT COUNT(*) FROM users;")
    row_count = cur.fetchone()[0]
    if row_count == 0:
        print("Table is empty. Populating database...")
        cursor.execute('INSERT INTO users (name, age, email) VALUES (%s, %s, %s)', ('Alice', 30, 'alice@mail.com'))
        cursor.execute('INSERT INTO users (name, age, email) VALUES (%s, %s, %s)', ('Bob', 25, 'bob@mail.com'))
        print("Database populated successfully.")
    else:
        print("Table already has data. Skipping population.")


with DatabaseConnection(database, user, password) as cursor:
    populate_db(cursor)

    # Query tp fetch DB content
    query = "SELECT * FROM users;"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)

