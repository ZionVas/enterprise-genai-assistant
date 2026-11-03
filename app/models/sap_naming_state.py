from typing import TypedDict


class SAPNamingState(TypedDict):
    original_code: str
    retrieved_context: str
    sources: list[dict]
    corrected_code: str