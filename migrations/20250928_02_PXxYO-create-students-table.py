"""
Create students table
"""

from yoyo import step

__depends__ = {'20250928_01_5H1Ey-create-classes-table'}

steps = [
    step("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_id INTEGER,
            FOREIGN KEY(class_id) REFERENCES classes(id)
        );
        """,
        "DROP TABLE IF EXISTS students;")
]
