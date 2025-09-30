import sqlite3
from typing import Annotated

from fastapi import Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies import requires_owner, requires_user
from structs import ClassRow, StudentCreate, StudentRow, UserRow
from templates import templates


async def new(
    request: Request,
    user: Annotated[UserRow, Depends(requires_user)]
    ) -> HTMLResponse:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    
    return templates.TemplateResponse(
        request=request,
        name="classes/new.html",
        context={"form_data": None, "form_errors": None}
    )

async def create(
    request: Request,
    user: Annotated[UserRow, Depends(requires_user)]
    ) -> Response:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    
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
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classes (name, owner_id) VALUES (?, ?)", (name, user.id))
        conn.commit()
    
    if request.headers.get("Hx-Request"):
        return Response(status_code=200, headers={"Hx-Redirect": "/"})

    return RedirectResponse(status_code=303, url="/")

async def show(
    request: Request,
    class_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> HTMLResponse:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")

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

async def edit(
    request: Request,
    class_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> HTMLResponse:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
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

async def delete(request: Request, class_id: int) -> Response:
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM classes WHERE id = ?", (class_id,))
    
    if request.headers.get("Hx-Request"):
        return Response(status_code=200, headers={"Hx-Redirect": f"/"})
    
    return RedirectResponse(status_code=303, url="/")

async def students(request: Request, class_id: int) -> Response:
    """Return the batch add student page"""
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name FROM classes WHERE id = {class_id};")
        class_row = ClassRow(*cursor.fetchone())

    return templates.TemplateResponse(
        request=request,
        name="classes/batch-add.html",
        context={"class": class_row}
    )
    

async def create_batch(request: Request, class_id: int) -> HTMLResponse:
    form_data = await request.form()
    students = form_data.get("students")
    
    if students.find(","):
        students = students.replace(",", "")

    students = students.split("\r\n")
    students = filter(None, students)

    batch_data = [StudentCreate(name=student, class_id=class_id) for student in students]
    
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO students (name, class_id) VALUES (?, ?)", batch_data)
        except Exception as e:
            print(f"an error occured when inserting students: {e}")

    return RedirectResponse(status_code=303, url=f"/classes/{class_id}/edit")


async def edit_student(request: Request, class_id: int, student_id: int):
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT id, name FROM classes WHERE id = {class_id};")
        class_row = ClassRow(*cursor.fetchone())

        cursor.execute(f"SELECT id, name, class_id FROM students WHERE id = {student_id};")
        student_row = StudentRow(*cursor.fetchone())

    return templates.TemplateResponse(
        request=request,
        name="classes/_edit-student.html",
        context={"class": class_row, "student": student_row}
    )
