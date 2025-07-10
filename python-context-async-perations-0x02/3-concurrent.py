import aiosqlite
import asyncio
from typing import Any


async def setup_database() -> None:
    """
    Asynchronously sets up the SQLite 'users' table and populates it with sample data.

    The table includes:
      - id: integer primary key
      - name: user's name
      - age: user's age
      - email: user's email address

    Inserts four example users after creating the table if it doesn't exist.
    """
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            )
        """)

        await db.executemany("""
            INSERT INTO users (name, age, email) VALUES (?, ?, ?)
        """, [
            ("Matt", 30, "alice@example.com"),
            ("Bobby", 50, "bob@example.com"),
            ("Carlos", 20, "charlie@example.com"),
            ("Dave", 24, "dave@example.com"),
            ("Steve", 42, "steve@example.com"),
            ("Viola", 45, "viola@example.com"),
        ])

        await db.commit()
        print("Database setup and sample data inserted successfully.")


# Run it
asyncio.run(setup_database())


async def async_fetch_users() -> list[tuple[Any]]:
    """
    Asynchronously fetches all users from the 'users' table.

    Returns:
        List of tuples, where each tuple represents a user record with columns (id, name, age, email).
    """
    async with aiosqlite.connect("users.db") as db:
        query = "SELECT * FROM users"
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            return rows

async def async_fetch_older_users() -> list[tuple[Any]]:
    """
    Asynchronously fetches users from the 'users' table whose age is greater than 40.

    Returns:
        List of tuples, each containing a user record (id, name, age, email) where age > 40.
    """
    async with aiosqlite.connect("users.db") as db:
        query = "SELECT * FROM users WHERE age > ?"
        parameter = 40,
        async with db.execute(query, parameter) as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently() -> None:
    """
    Runs both user-fetching functions concurrently and prints their results.
    
    Combines the results from:
      - async_fetch_users: all users
      - async_fetch_older_users: users older than 40
    Returns:
        None
    """
    tasks = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    for result in tasks:
        print(result)

    return

asyncio.run(fetch_concurrently())

