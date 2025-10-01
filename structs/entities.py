from collections import namedtuple

UserRow = namedtuple("UserRow", ["id", "email"])

ClassRow = namedtuple("ClassRow", ["id", "name"])

ClassOwnerRow = namedtuple("ClassRow", ["id", "name", "owner_id"])

StudentRow = namedtuple("StudentRow", ["id", "name", "class_id"])

StudentCreate = namedtuple("StudentCreate", ["name", "class_id"])

SessionRow = namedtuple("SessionRow", ["id", "token", "user_id", "expires_at"])

SessionCreate = namedtuple("SessionCreate", ["token", "user_id", "expires_at"])