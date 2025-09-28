from fastapi import APIRouter

from controller import get_class_edit, get_homepage, get_class_detail, make_teams

router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'tags', 'dependencies')
routes = [
    ("GET",     "/",                                get_homepage,       None, None),

    ("GET",     "/classes/{class_id}",              get_class_detail,   None, None),
    ("GET",     "/classes/{class_id}/edit",         get_class_edit,     None, None),

    ("POST",    "/make-teams",                      make_teams,         None, None)
]

for method, path, handler, tags, deps in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
        tags=tags,
        dependencies=deps or None
    )


