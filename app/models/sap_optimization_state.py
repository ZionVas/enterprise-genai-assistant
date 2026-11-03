from typing import TypedDict


class SAPOptimizationState(TypedDict):
    original_code: str
    retrieved_context: str
    sources: list[dict]
    optimized_code: str
    validation_errors: list[str]
    iteration: int
    validation_passed: bool