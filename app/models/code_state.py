from typing import TypedDict


class CodeGenerationState(TypedDict):
    user_request: str
    language: str
    retrieved_context: str
    sources: list[dict]
    response: str