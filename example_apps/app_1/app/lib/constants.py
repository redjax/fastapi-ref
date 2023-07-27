"""Define objects that can be shared/imported throughout application.

Use globals sparingly.
"""
from enum import Enum


## Build an enum of tags
#  https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags-with-enums
class Tags(Enum):
    items = "items"
    users = "users"
