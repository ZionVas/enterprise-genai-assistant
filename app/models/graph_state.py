from typing import TypedDict


class GenerationState(TypedDict):
    user_input: str
    response: str