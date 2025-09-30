import sqlite3

from fastapi import Request
from structs import ClassOwnerRow, UserRow


def requires_user(request: Request):
    session_token = request.cookies.get("session-id")

    if not session_token:
        return None
    
    # TODO: get session from db
    # and use that user_id to look up the user
    
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM users WHERE email = ?", (session_token, ))

        user = UserRow(*cursor.fetchone())

    return user


def requires_owner(request: Request, class_id: int):
    session_token = request.cookies.get("session-id")

    if not session_token:
        return None
    
    # TODO: get session from db
    # and use that user_id to look up the user
    
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM users WHERE email = ?", (session_token, ))

        user = UserRow(*cursor.fetchone())

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, owner_id FROM classes WHERE id = ?", (class_id,))
        class_row = ClassOwnerRow(*cursor.fetchone())

        if user.id != class_row.owner_id:
            return None
        
    return user
