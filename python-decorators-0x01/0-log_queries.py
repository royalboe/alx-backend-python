import sqlite3
from datetime import datetime
import functools
import logging

# Configure logging to log to a file
logging.basicConfig(
   level=logging.INFO, 
   format='%(asctime)s - %(levelname)s - %(message)s', 
   handlers=[
       logging.FileHandler('db_queries.log'),
       logging.StreamHandler()
   ],
)

def log_queries(func):
  @functools.wraps(func)  # Preserve the original function's name and docstring
  def wrapper(*args, **kwargs):
    query = kwargs.get('query') or (args[0] if args else "")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Executing query: {query} at {timestamp}")
    return func(*args, **kwargs)    
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

users = fetch_all_users(query="SELECT * FROM users")

if __name__ == "__main__":
    print(users)