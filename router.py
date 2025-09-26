from fastapi import APIRouter

from controller import get_homepage, get_class_detail, get_make_teams, make_teams

router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'tags', 'dependencies')
routes = [
    ("GET",     "/",                                get_homepage,       None, None),

    ("GET",     "/classes/{class_id}",              get_class_detail,   None, None),
    ("GET",     "/classes/{class_id}/make-teams",   get_make_teams,     None, None),
    ("POST",    "/classes/{class_id}/make-teams",   make_teams,         None, None)
]

for method, path, handler, tags, deps in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
        tags=tags,
        dependencies=deps or None
    )


