"""
Create classes table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """,
        "DROP TABLE classes;"
    )
]
