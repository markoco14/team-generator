import sqlite3
import random

from faker import Faker

from structs import ClassRow


def seed_users() -> None:
    data = [
        ("test1@testmail.com", "test1234"),
        ("test2@testmail.com", "test1234"),
        ("test3@testmail.com", "test1234"),
        ("test4@testmail.com", "test1234"),
        ("test5@testmail.com", "test1234")
    ]

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO users (email, password) VALUES (?, ?)", data)
        except Exception as e:
            print(f"an error occured inserting users: {e}")

    print("Successfully seeded DB with users")


def seed_classes() -> None:
    data = [
        ("Canary", 1),
        ("Crow", 1),
        ("Bluejay", 2),
        ("Goose", 2),
        ("Ostrich", 3),
    ]

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO classes (name, owner_id) VALUES (?, ?);", data)
        except Exception as e:
            print(f"An error occured inserting classes: {e}")

    print("Successfully seeded DB with classes")

def seed_students():
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM classes;")
        class_groups = [ClassRow(*row) for row in cursor.fetchall()]

        fake = Faker()
        students = []
        for class_group in class_groups:
            for _ in range(random.randint(10, 15)):
                students.append((fake.name(), class_group.id))
        try:
            cursor.executemany("INSERT INTO students (name, class_id) VALUES (?, ?)", students)
        except Exception as e:
            print(f"An error occured inserting students: {e}")

    print("Successfully seeded DB with students")

def list_classes():
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM classes;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    print(rows)
    for row in rows:
        print(f"row: {row}")
        print(f"id: {row[0]}")
        print(f"name: {row[1]}")
