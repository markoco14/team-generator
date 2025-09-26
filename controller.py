from fastapi import Request
from fastapi.responses import HTMLResponse

from templates import templates


async def get_homepage(request: Request) -> HTMLResponse:
    classes_param = request.query_params.get("classes")

    classes = None
    if classes_param == "many":
        classes = [
            "Class A",
            "Class B",
            "Class C",
            "Class D",
            "Class E",
            "Class F"
        ]
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

    students = None
    if students_param == "many":
        students = [
            "Student A",
            "Student B",
            "Student C",
            "Student D",
            "Student E"
        ]
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
        "Student E"
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="make-teams.html",
        context={"students": students}
    )


async def make_teams(request: Request) -> HTMLResponse:
    form_data = await request.form()
    students = form_data.getlist("students")
    
    return templates.TemplateResponse(
        request=request,
        name="_teams.html",
        context={"students": students}
    )