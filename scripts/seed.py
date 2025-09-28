import sqlite3

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
# list_classes()