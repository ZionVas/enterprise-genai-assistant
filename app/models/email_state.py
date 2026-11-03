from typing import TypedDict


class EmailState(TypedDict):
    recipient: str
    purpose: str
    key_points: str
    tone: str
    length: str
    response: str