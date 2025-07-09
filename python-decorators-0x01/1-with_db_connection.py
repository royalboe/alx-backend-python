import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_connect(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn=conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper_connect

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

user = get_user_by_id(user_id=1)

print(user)