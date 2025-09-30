import sqlite3
from structs import ClassOwnerRow, UserRow


def requires_user():
    # needs logic to get user from session
    return UserRow(id=1)

def requires_owner(class_id: int):
    # needs logic to get user from session
    user = UserRow(id=1)

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, owner_id FROM classes WHERE id = ?", (class_id,))
        class_row = ClassOwnerRow(*cursor.fetchone())

        if user.id != class_row.owner_id:
            return None
        
    return UserRow(id=1)