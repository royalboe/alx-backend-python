import mysql.connector as connector
from mysql.connector import Error
from typing import Any

class ExecuteQuery:
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
                query (str): Query to execute
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
                self.cursor = self.cnx.cursor()
                return self
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

    def execute_query(self, query: str, parameters: tuple[Any, ...]|None = None) -> list[tuple]:
        """
        Execute a query with optional parameters.

        Args:
            query (str): SQL query string.
            parameters (Optional[Tuple[Any]]): Parameters to substitute in query.

        Returns:
            list[tuple]: Result set as list of tuples.
        """
        if not self.cursor:
            print("No cursor")
            raise RuntimeError("Cursor is not initialized.")

        if parameters:
            print("Paramters present")
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)

        if query.strip().upper().startswith("SELECT"):
            return self.cursor.fetchall()
        return []

user = 'prodev'
password = 'password123'
host = 'localhost'
database = 'ALX_prodev'

with ExecuteQuery(database, user, password) as executor:
    # Query tp fetch DB content
    query = "SELECT * FROM users WHERE age > %s"
    parameter = (49,)
    result = executor.execute_query(query, parameter)

    print(result)