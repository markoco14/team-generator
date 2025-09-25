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