from collections import namedtuple

ClassRow = namedtuple("ClassRow", ["id", "name"])

StudentRow = namedtuple("StudentRow", ["id", "name", "class_id"])