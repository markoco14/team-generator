import sqlite3

from fastapi import Request
from structs import ClassOwnerRow, UserRow

USER_ID = 1

def requires_user(request: Request):
    session_token = request.cookies.get("session-id")

    if not session_token:
        return None
    
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM users WHERE email = ?", (session_token, ))

        user = UserRow(*cursor.fetchone())

    return user

def requires_owner(class_id: int):
    # needs logic to get user from session
    user = UserRow(id=USER_ID)

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, owner_id FROM classes WHERE id = ?", (class_id,))
        class_row = ClassOwnerRow(*cursor.fetchone())

        if user.id != class_row.owner_id:
            return None
        
    return user
