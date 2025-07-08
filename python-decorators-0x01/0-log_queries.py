import sqlite3
from datetime import datetime


def log_queries(func):
  def wrapper(*args, **kwargs):
    result = func(*args, **kwargs)
    if kwargs and args:
      print(f"{datetime.now()}: {args} and keyword arguments: {kwargs}")
    elif kwargs:
      print(f"{datetime.now()}: keyword arguments: {kwargs}")
    else:
      print(f"{datetime.now()}: {args}")
    return result
  return wrapper

def populate_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))
    conn.commit()
    conn.close()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

populate_db()

users = fetch_all_users("SELECT * FROM users")

if __name__ == "__main__":
    print(users)