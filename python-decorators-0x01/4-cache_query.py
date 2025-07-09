import inspect
import time
import sqlite3 
import functools
from typing import Callable, Any


query_cache = {}

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


def cache_query(func: Callable) -> Callable:
    """
    Decorator that caches query results to avoid repeated database calls for the same query.

    Args:
        func: The function to decorate.

    Returns:
        Callable: The wrapped function with an active database connection passed as an argument.

    """
    # Inspect the function signature and bound argument names with their parameters
    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        # Get the key query from the arguments dictionary
        query = bound.arguments.get("query")
        if query is None:
            raise ValueError("The 'query' parameter must be provided for caching.")

        if query not in query_cache:
            print("Putting in cache...")
            try:
                query_cache[query] = func(*args, **kwargs)
            except Exception as e:
                print(f"Error processing: {e}")
                raise
        return query_cache[query]
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn: sqlite3.Connection, query: str) -> list|None:
    """
        Fetch users based on the provided SQL query and cache the result.

        Args:
            conn: SQLite connection object automatically provided by decorator.
            query: SQL query string to execute.

        Returns:
            List of tuples containing query results.
        """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)