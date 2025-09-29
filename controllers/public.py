import math
import random
import sqlite3
from typing import Annotated

from fastapi import Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies import requires_user
from structs import ClassRow, UserRow
from templates import templates


async def get_homepage(
    request: Request,
    user: Annotated[UserRow, Depends(requires_user)]
    ) -> HTMLResponse:
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"user": user, "classes": None}
        )

    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM classes WHERE owner_id = ?;", (user.id,))
        classes = [ClassRow(*row) for row in cursor.fetchall()]
        cursor.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user": user, "classes": classes}
    )


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