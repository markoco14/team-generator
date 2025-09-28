import math
import random

from fastapi import Request, Response
from fastapi.responses import HTMLResponse

from templates import templates


async def get_homepage(request: Request) -> HTMLResponse:
    classes_param = request.query_params.get("classes")

    classes = [
        "Class A",
        "Class B",
        "Class C",
        "Class D",
        "Class E",
        "Class F"
    ]
    if classes_param == "none":
        classes = None
    elif classes_param == "one":
        classes = [
            "Class A",
        ]
        
    # elif request.query
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"classes": classes}
    )


async def get_class_detail(request: Request) -> HTMLResponse:
    students_param = request.query_params.get("students")

    students = [
        "Student A",
        "Student B",
        "Student C",
        "Student D",
        "Student E"
    ]
    if students_param == "none":
        students = None
    elif students_param == "one":
        students = [
            "Student A"
        ]

    return templates.TemplateResponse(
        request=request,
        name="classes-show.html",
        context={"students": students}
    )


async def get_make_teams(request: Request) -> HTMLResponse:
    
    students = [
        "Student A",
        "Student B",
        "Student C",
        "Student D",
        "Student E",
        "Student F",
        "Student G",
        "Student H",
        "Student I",
        "Student J",
        "Student K",
        "Student L",
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="make-teams.html",
        context={"students": students}
    )


async def make_teams(request: Request) -> HTMLResponse:
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