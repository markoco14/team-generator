import sqlite3
from fastapi import Request, Response


def delete(request: Request, student_id: int) -> Response:
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    return Response(status_code=200, content="Student deleted successfully")