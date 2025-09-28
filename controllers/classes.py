import sqlite3

from fastapi import Request, Response
from fastapi.responses import HTMLResponse

from structs import StudentRow
from templates import templates


async def new(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="classes/new.html"
    )

async def show(request: Request, class_id: int) -> HTMLResponse:
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name, class_id FROM students WHERE class_id = {class_id};")
        students = [StudentRow(*row) for row in cursor.fetchall()]
        cursor.close()

    return templates.TemplateResponse(
        request=request,
        name="classes/show.html",
        context={"students": students}
    )

async def edit(request: Request, class_id: int) -> HTMLResponse:
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name, class_id FROM students WHERE class_id = {class_id};")
        students = [StudentRow(*row) for row in cursor.fetchall()]
        cursor.close()
    
    return templates.TemplateResponse(
        request=request,
        name="classes/edit.html",
        context={"students": students}
    )