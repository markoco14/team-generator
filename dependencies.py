import sqlite3

from fastapi import Request
from structs import ClassOwnerRow, SessionRow, UserRow


def requires_user(request: Request):
    session_token = request.cookies.get("session-id")

    if not session_token:
        return None
    
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, token, user_id, expires_at FROM sessions WHERE token = ?", (session_token,))
        session = cursor.fetchone()

    if not session:
        return None

    session = SessionRow(*session)
    
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM users WHERE id = ?", (session.user_id, ))

        user = cursor.fetchone()

    if not user:
        return None

    user = UserRow(*user)

    return user


def requires_owner(request: Request, class_id: int):
    session_token = request.cookies.get("session-id")

    if not session_token:
        return None
    
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, token, user_id, expires_at FROM sessions WHERE token = ?", (session_token,))
        session = cursor.fetchone()

    if not session:
        return None

    session = SessionRow(*session)
    
    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM users WHERE id = ?", (session.user_id, ))

        user = cursor.fetchone()

    if not user:
        return None

    user = UserRow(*user)

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, owner_id FROM classes WHERE id = ?", (class_id,))
        class_row = ClassOwnerRow(*cursor.fetchone())

        if user.id != class_row.owner_id:
            return None
        
    return user
