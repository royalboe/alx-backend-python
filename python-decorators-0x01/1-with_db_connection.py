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

@with_db_connection
def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> tuple | None:
    """
    Gets a user by ID.

    Args:
        conn: SQLite connection object provided by decorator.
        user_id: The id of the user to retrieve.

    Returns:
        A tuple representing the user row if found, otherwise None
    """
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

user = get_user_by_id(user_id=1)

print(user)