import sqlite3
import functools
from typing import Callable, Any

def with_db_connection(func: Callable) -> Callable:
    """
    A decorator that opens a SQLite database connection and closes it automatically.

    Args:
        func: The function to be passed to the decorator.

    Returns:
        The wrapped function with an active database connection passed as an argument.
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


def transactional(func: Callable) -> Callable:
    """
        A decorator that manages database transactions by automatically committing or rolling back changes.

        Args:
            func: Function to be passed to the decorator.

        Returns:
            The wrapped function.

    """

    @functools.wraps(func)
    def wrapper(conn: sqlite3.Connection, *args: Any, **kwargs: Any) -> Any:
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            print(f"Error processing request: {e}")
            conn.rollback()
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn: sqlite3.Connection, user_id: int, new_email: str) -> None:
    """
        Update a user's email address in the database.

        Args:
            conn: SQLite connection object automatically provided by decorators.
            user_id: The ID of the user to update.
            new_email: The new email address to set.

        Returns:
            None
        """
    cursor = conn.cursor()
    query = "UPDATE users SET email = ? WHERE id = ?"
    cursor.execute(query, (new_email, user_id))
    return


#### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')