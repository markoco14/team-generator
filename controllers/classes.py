import sqlite3
from typing import Annotated

from fastapi import Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies import requires_owner, requires_user
from structs.entities import ClassRow, StudentCreate, StudentRow, UserRow
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
        context={"user": user, "form_data": None, "form_errors": None}
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
        
        cursor.execute("SELECT * FROM classes WHERE id = ?;", (class_id, ))
        class_row = cursor.fetchone()
        
        cursor.execute(f"SELECT id, name, class_id FROM students WHERE class_id = {class_id};")
        students = [StudentRow(*row) for row in cursor.fetchall()]
        
        cursor.close()

    return templates.TemplateResponse(
        request=request,
        name="classes/show.html",
        context={"user": user, "class": class_row, "students": students}
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
        context={"user": user, "class": class_row, "students": students}
    )

async def update(
    request: Request,
    class_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> HTMLResponse:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    
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

async def delete(
    request: Request,
    class_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> Response:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM classes WHERE id = ?", (class_id,))
    
    if request.headers.get("Hx-Request"):
        return Response(status_code=200, headers={"Hx-Redirect": f"/"})
    
    return RedirectResponse(status_code=303, url="/")

async def students(
    request: Request,
    class_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> Response:
    """Return the batch add student page"""
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")

    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name FROM classes WHERE id = {class_id};")
        class_row = ClassRow(*cursor.fetchone())

    return templates.TemplateResponse(
        request=request,
        name="classes/batch-add.html",
        context={"user": user, "class": class_row}
    )


async def input(request: Request, class_id: int):
    return templates.TemplateResponse(
        request=request,
        name="classes/_student-input.html",
        context={"class_id": class_id}
    )


async def delete_input(request: Request):
    return Response(status_code=200, content="Input deleted.")
    

async def create_batch(
    request: Request,
    class_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> HTMLResponse:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    
    form_data = await request.form()
    students = form_data.getlist("students")

    error = None
    count = 0
    for student in students:
        if not student:
            count += 1

    if count == 1:
        error = f"{count} student has no name."
    elif count > 1:
        error = f"{count} students have no name."

    if error:
        html = f"{error}"
        return HTMLResponse(
            status_code=200,
            content=html,
            headers={
                "hx-retarget": ".error",
                "hx-reswap": "innerHTML"
                })
    
    students = filter(None, students)

    batch_data = [StudentCreate(name=student, class_id=class_id) for student in students]
    
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO students (name, class_id) VALUES (?, ?)", batch_data)
        except Exception as e:
            print(f"an error occured when inserting students: {e}")
        
    if request.headers.get("hx-request"):
        response = Response(status_code=200, headers={"hx-redirect": f"/classes/{class_id}/edit"})
    else:
        response = RedirectResponse(status_code=303, url=f"/classes/{class_id}/edit")

    return response


async def edit_student(
    request: Request,
    class_id: int,
    student_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> HTMLResponse:
    """Returns the inline edit student form"""
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT id, name FROM classes WHERE id = {class_id};")
        class_row = ClassRow(*cursor.fetchone())

        cursor.execute(f"SELECT id, name, class_id FROM students WHERE id = {student_id};")
        student_row = StudentRow(*cursor.fetchone())

    return templates.TemplateResponse(
        request=request,
        name="classes/_edit-student.html",
        context={"user": user, "class": class_row, "student": student_row}
    )


async def update_student(
    request: Request,
    student_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> Response:
    """
    Updates a student resource.
    Only exposes updating the name as students can't be moved between classes.
    Triggers a page refresh with the response.
    """
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    
    form_data = await request.form()
    name = form_data.get("student")

    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE STUDENTS SET name = ? WHERE id = ?", (name, student_id,))

    return Response(status_code=200, headers={"Hx-Refresh": "true"})


async def delete_student(
    request: Request,
    student_id: int,
    user: Annotated[UserRow, Depends(requires_owner)]
    ) -> Response:
    """
    Deletes a student resource.
    Responds with a response. No visible client side confirmation except the student disappearing, for now.
    """
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    return Response(status_code=200, content="Student deleted successfully")


async def teams(
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
        name="classes/teams.html",
        context={"user": user, "students": students}
    )