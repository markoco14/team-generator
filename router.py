from fastapi import APIRouter

from controllers import classes, public

router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'tags', 'dependencies')
routes = [
    ("GET",     "/",                                    public.get_homepage,    None, None),

    ("POST",    "/classes",                             classes.create,         None, None),
    ("GET",     "/classes/new",                         classes.new,            None, None),
    ("GET",     "/classes/{class_id}",                  classes.show,           None, None),
    ("GET",     "/classes/{class_id}/edit",             classes.edit,           None, None),
    ("PUT",     "/classes/{class_id}",                  classes.update,         None, None),
    ("DELETE",  "/classes/{class_id}",                  classes.delete,         None, None),
    ("GET",     "/classes/{class_id}/delete",           classes.delete,         None, None),
    ("GET",     "/classes/{class_id}/students",         classes.students,       None, None),
    ("POST",    "/classes/{class_id}/students/batch",   classes.create_batch,  None, None),

    ("POST",    "/make-teams",                      public.make_teams,      None, None)
]

for method, path, handler, tags, deps in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
        tags=tags,
        dependencies=deps or None
    )


