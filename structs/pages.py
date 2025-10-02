from typing import List, TypedDict

from structs.entities import ClassRow, UserRow


class HomePageData(TypedDict):
    user: UserRow
    classes: List[ClassRow]
    form_values: dict
    form_errors: dict
    