"""
Create sessions table
"""

from yoyo import step

__depends__ = {'20250929_01_rMjNO-initial'}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL,
            expires_at INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """,
        "DROP TABLE IF EXISTS sessions;"
    )
]
