from fastapi import APIRouter, Depends

from controllers import classes, public
from dependencies import requires_owner, requires_user

router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'dependencies')
routes = [
    ("GET",     "/",                                                public.get_homepage,    [Depends(requires_user)]),
    ("POST",    "/make-teams",                                      public.make_teams,      [Depends(requires_user)]),

    ("POST",    "/classes",                                         classes.create,         [Depends(requires_user)]),
    ("GET",     "/classes/new",                                     classes.new,            [Depends(requires_user)]),
    ("GET",     "/classes/{class_id}",                              classes.show,           [Depends(requires_owner)]),
    ("GET",     "/classes/{class_id}/edit",                         classes.edit,           [Depends(requires_owner)]),
    ("PUT",     "/classes/{class_id}",                              classes.update,         [Depends(requires_owner)]),
    ("DELETE",  "/classes/{class_id}",                              classes.delete,         [Depends(requires_owner)]),
    ("GET",     "/classes/{class_id}/delete",                       classes.delete,         [Depends(requires_owner)]),
    ("GET",     "/classes/{class_id}/students",                     classes.students,       [Depends(requires_owner)]),
    ("POST",    "/classes/{class_id}/students/batch",               classes.create_batch,   [Depends(requires_owner)]),
    ("GET",     "/classes/{class_id}/students/{student_id}/edit",   classes.edit_student,   [Depends(requires_owner)]),
    ("PUT",     "/classes/{class_id}/students/{student_id}",        classes.update_student, [Depends(requires_owner)]),
    ("DELETE",  "/classes/{class_id}/students/{student_id}",        classes.delete_student, [Depends(requires_owner)]),
]

for method, path, handler, deps in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
        dependencies=deps or None
    )


