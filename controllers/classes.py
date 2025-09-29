import sqlite3

from fastapi import Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from structs import ClassRow, StudentRow
from templates import templates


async def new(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="classes/new.html",
        context={"form_data": None, "form_errors": None}
    )

async def create(request: Request) -> Response:
    form_data = await request.form()
    name = form_data.get("name")

    form_errors = None
    if not name:
        form_errors = {"name": "You need to give the class a name."}
    elif len(name) < 2:
        form_errors = {"name": "The name needs to be longer than two characters."}
    
    if form_errors:
        return templates.TemplateResponse(
            request=request,
            name="classes/new.html",
            headers={"Hx-Reselect": "#name-error", "Hx-Retarget": "#name-error", "Hx-Reswap": "outerHTML"},
            context={"form_data": form_data, "form_errors": form_errors}
        )
    
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classes (name) VALUES (?)", (name,))
        conn.commit()
    
    if request.headers.get("Hx-Request"):
        return Response(status_code=200, headers={"Hx-Redirect": "/"})

    return RedirectResponse(status_code=303, url="/")

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
        cursor.execute(f"SELECT id, name FROM classes WHERE id = {class_id};")
        class_row = ClassRow(*cursor.fetchone())
        cursor.execute(f"SELECT id, name, class_id FROM students WHERE class_id = {class_id};")
        students = [StudentRow(*row) for row in cursor.fetchall()]
        cursor.close()
    
    return templates.TemplateResponse(
        request=request,
        name="classes/edit.html",
        context={"class": class_row, "students": students}
    )

async def update(request: Request, class_id: int) -> HTMLResponse:
    form_data = await request.form()
    name = form_data.get('name')

    form_errors = None
    if not name:
        form_errors = {"name": "You need to give the class a name."}
    elif len(name) < 2:
        form_errors = {"name": "The name needs to be longer than two characters."}
    
    if form_errors:
        return Response(status_code=200, headers={"Hx-Refresh": "true"})
        # return templates.TemplateResponse(
        #     request=request,
        #     name="classes/new.html",
        #     headers={"Hx-Reselect": "#name-error", "Hx-Retarget": "#name-error", "Hx-Reswap": "outerHTML"},
        #     context={"form_data": form_data, "form_errors": form_errors}
        # )
    
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE CLASSES SET name = ? WHERE id = ?", (name, class_id))

    return Response(status_code=200, headers={"Hx-Refresh": "true"})