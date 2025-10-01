import math
import random
import sqlite3
import time
from typing import Annotated
import uuid

from email_validator import validate_email
from fastapi import Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies import requires_user
from structs.structs import ClassRow, SessionCreate, UserRow
from structs.pages import HomePageData
from templates import templates
from utils import verify_password


async def get_homepage(
    request: Request,
    user: Annotated[UserRow, Depends(requires_user)]
    ) -> HTMLResponse:
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context=HomePageData(
                user=None,
                classes=None,
                form_values=None,
                form_errors=None
            )
        )

    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM classes WHERE owner_id = ?;", (user.id,))
        classes = [ClassRow(*row) for row in cursor.fetchall()]
        cursor.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=HomePageData(
            user=user,
            classes=classes,
            form_values=None,
            form_errors=None
        )
    )


async def login(request: Request):
    form_data = await request.form()
    email = form_data.get("username")
    password = form_data.get("password")

    form_errors = {}
    if not email:
        form_errors["email"] = "You need an email"

    if not form_errors:
        try:
            validate_email(email)
        except Exception as e:
            form_errors["email"] = "This email isn't valid"

    if not password:
        form_errors["password"] = "You need a password"

    if form_errors:
        if request.headers.get("hx-request"):
            response = templates.TemplateResponse(
                request=request,
                name="index.html",
                headers={"hx-reswap": "innerHTML", "hx-retarget": "body"},
                context=HomePageData(
                    user=None,
                    classes=None,
                    form_values=form_data,
                    form_errors=form_errors
                )
            )
        else:
            response = RedirectResponse(status_code=303, url="/")
        return response

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
    
    if not user:
        form_errors["password"] = "Email or password is incorrect."
        if request.headers.get("hx-request"):
            response = templates.TemplateResponse(
                request=request,
                name="index.html",
                headers={"hx-reswap": "innerHTML", "hx-retarget": "body"},
                context=HomePageData(
                    user=None,
                    classes=None,
                    form_values=form_data,
                    form_errors=form_errors
                )
            )
        else:
            response = RedirectResponse(status_code=303, url="/")
        return response
    
    password_verified = await verify_password(user[2], password)
    if not password_verified:
        form_errors["password"] = "Email or password is incorrect."

    if form_errors:
        if request.headers.get("hx-request"):
            response = templates.TemplateResponse(
                request=request,
                name="index.html",
                headers={"hx-reswap": "innerHTML", "hx-retarget": "body"},
                context=HomePageData(
                    user=None,
                    classes=None,
                    form_values=form_data,
                    form_errors=form_errors
                )
            )
        else:
            response = RedirectResponse(status_code=303, url="/")
        return response
    
    user = UserRow(id=user[0], email=user[1])
    token = str(uuid.uuid4())
    expires_at = int(time.time()) + 3600
    new_session = SessionCreate(token=token, user_id=user.id, expires_at=expires_at)

    with sqlite3.connect("db.sqlite3") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)", (new_session.token, new_session.user_id, new_session.expires_at))

    if request.headers.get("hx-request"):
        response = Response(status_code=200, headers={"hx-redirect": "/"})
    else:
        response = RedirectResponse(status_code=303, url="/")

    response.set_cookie(key="session-id", value=token)
    return response


async def logout(request: Request):
    response = RedirectResponse(status_code=303, url="/")
    if request.cookies.get("session-id"):
        response.delete_cookie(key="session-id")
    return response


async def make_teams(
    request: Request,
    user: Annotated[UserRow, Depends(requires_user)]
    ) -> HTMLResponse:
    if not user:
        if request.headers.get("Hx-Request"):
            return Response(status_code=401, headers={"Hx-Redirect": "/"})
        
        return RedirectResponse(status_code=303, url="/")

    form_data = await request.form()
    number_of_teams = form_data.get("number-of-teams")
    students = form_data.getlist("students")

    if not number_of_teams:
        return Response(status_code=422, content="Number of teams not found in form submission.")
    
    # turn number_of_teams into int value to use as int later
    number_of_teams = int(number_of_teams)

    if number_of_teams < 2:
        return Response(status_code=422, content="Number of teams needs to be a number greater than 2.")
    
    if number_of_teams > math.floor(len(students) / 2):
        return Response(status_code=422, content=f"Number of teams cannot be more than {math.floor(len(students) / 2)}.")
    
    # shuffles 'students' in place: does not create new variable
    random.shuffle(students) 
    
    # this implementation handles it perfectly
    # extra students will always be put in a team
    # starting from team 1
    # if you want to randomly assign remainder students (so team 5 might be the team with the extra member)
    # need to remove the remainder students first
    teams = []
    for i in range(number_of_teams):
        team = students[i::number_of_teams]
        teams.append(team)
    
    return templates.TemplateResponse(
        request=request,
        name="_teams.html",
        context={"teams": teams}
    )