from fastapi import APIRouter

from controller import get_homepage

router = APIRouter()

# routes follow ('method', '/route', 'handler', 'tags', 'dependencies')
routes = [
    ("GET", "/",  get_homepage, None, None),
]

for method, path, handler, tags, deps in routes:
    router.add_api_route(
        path,
        handler,
        methods=[method],
        tags=tags,
        dependencies=deps or None
    )


