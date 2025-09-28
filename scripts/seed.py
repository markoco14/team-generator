import sqlite3
import random

from faker import Faker

from structs import ClassRow


def seed_classes() -> None:
    data = [
        ("Class A",),
        ("Class B",),
        ("Class C",),
        ("Class D",),
        ("Class E",),
    ]
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO classes (name) VALUES (?);", data)
        except Exception as e:
            print(f"An error occured inserting classes: {e}")
        cursor.close()
        conn.commit()

    print("DB seeded with classes")

def seed_students():
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM classes;")
        class_groups = [ClassRow(*row) for row in cursor.fetchall()]
        fake = Faker()
        students = []
        for class_group in class_groups:
            for i in range(random.randint(10, 15)):
                students.append((fake.name(), class_group.id))
        try:
            cursor.executemany("INSERT INTO students (name, class_id) VALUES (?, ?)", students)
            conn.commit()
        except Exception as e:
            print(f"An error occured inserting students: {e}")

    print("DB seeded with students")

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

# seed_classes()
# seed_students()
# list_classes()