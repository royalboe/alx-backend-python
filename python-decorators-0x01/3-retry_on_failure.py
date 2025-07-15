import time
import sqlite3
import functools
from typing import Callable, Any

class RetryFailedException(Exception):
    """
    Exception raised when all retry attempts for an operation fail.

    Attributes:
        message (str): Explanation of the error and context.
        original_exception (Exception, optional): The original exception that caused the final failure.
    """

    def __init__(self, message: str, original_exception: Exception=None):
        """
        Initialize RetryFailedException.

        Args:
            message (str): Human-readable error message describing the failure.
            original_exception (Exception, optional): The last exception encountered during retries. Defaults to None.
        """
        super().__init__(message)
        self.original_exception = original_exception
        print(f"{self.original_exception}".upper())


def with_db_connection(func: Callable) -> Callable:
    """
    A decorator that opens a SQLite database connection and closes it automatically.

    Args:
        func: The function to be passed to the decorator.

    Returns:
        Callable: The wrapped function with an active database connection passed as an argument.
    """
    @functools.wraps(func)
    def wrapper_connect(*args: Any, **kwargs: Any) -> Any:
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn=conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper_connect

def retry_on_failure(retries: int, delay: int) -> Callable:
    """

    Args:
        retries: Maximum number of retry attempts before giving up.
        delay: Delay in seconds between attempts.

    Returns:
        Callable: The wrapped function with retry logic.
    """
    def transactional(func: Callable) -> Callable:
        """
            A decorator that manages database transactions, committing on success and rolling back on failure.
            Retries the function up to 'retries' times in case of exceptions.

            Args:
                func: Function to be passed to the decorator.

            Returns:
                Callable: The wrapped function with transaction and retry logic.

        """

        @functools.wraps(func)
        def wrapper(conn: sqlite3.Connection, *args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(retries):
                print("Attempting to process request...", attempt + 1)
                try:
                    result = func(conn, *args, **kwargs)
                    conn.commit()
                    return result
                except Exception as e:
                    conn.rollback()
                    last_exception = e
                    print(f"Error processing request retrying in {delay} seconds...")
                    time.sleep(delay)
            else:
                raise RetryFailedException(f"Max retries({retries}) reached persistent errors in retry", last_exception)    

        return wrapper
    return transactional


@with_db_connection
@retry_on_failure(retries=3, delay=2)
def fetch_users_with_retry(conn: sqlite3.Connection) -> list | None:
    """
        Fetch all users from the 'users' table with automatic transaction handling and retry on failure.

        Args:
            conn: SQLite connection object provided by the decorators.

        Returns:
            A list of tuples representing user rows if successful, otherwise None.
        """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user;")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)