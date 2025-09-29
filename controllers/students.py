import sqlite3
from fastapi import Request, Response

async def update(request: Request, student_id: int):
    """
    Updates a student resource.
    Only exposes updating the name as students can't be moved between classes.
    Triggers a page refresh with the response.
    """
    form_data = await request.form()
    name = form_data.get("student")

    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE STUDENTS SET name = ? WHERE id = ?", (name, student_id,))

    return Response(status_code=200, headers={"Hx-Refresh": "true"})


async def delete(request: Request, student_id: int) -> Response:
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    return Response(status_code=200, content="Student deleted successfully")