from fastapi import APIRouter, Depends

from controllers import classes, public, students
from dependencies import requires_user

router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'dependencies')
routes = [
    ("GET",     "/",                                                public.get_homepage,    [Depends(requires_user)]),
    ("POST",    "/make-teams",                                      public.make_teams,      None),

    ("POST",    "/classes",                                         classes.create,         None),
    ("GET",     "/classes/new",                                     classes.new,            None),
    ("GET",     "/classes/{class_id}",                              classes.show,           None),
    ("GET",     "/classes/{class_id}/edit",                         classes.edit,           None),
    ("PUT",     "/classes/{class_id}",                              classes.update,         None),
    ("DELETE",  "/classes/{class_id}",                              classes.delete,         None),
    ("GET",     "/classes/{class_id}/delete",                       classes.delete,         None),
    ("GET",     "/classes/{class_id}/students",                     classes.students,       None),
    ("POST",    "/classes/{class_id}/students/batch",               classes.create_batch,   None),
    ("GET",     "/classes/{class_id}/students/{student_id}/edit",   classes.edit_student,   None),

    ("PUT",     "/students/{student_id}",                           students.update,        None),
    ("DELETE",  "/students/{student_id}",                           students.delete,        None),

]

for method, path, handler, deps in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
        dependencies=deps or None
    )


