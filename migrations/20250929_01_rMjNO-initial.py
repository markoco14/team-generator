"""
Initial
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """,
        "DROP TABLE IF EXISTS users;"
        ),
    step("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner_id INTEGER,
            FOREIGN KEY(owner_id) REFERENCES users(id)
        );
        """,
        "DROP TABLE IF EXISTS classes;"
        ),
    step("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_id INTEGER,
            FOREIGN KEY(class_id) REFERENCES classes(id)
        );""",
        "DROP TABLE IF EXISTS students;"
        )
]
