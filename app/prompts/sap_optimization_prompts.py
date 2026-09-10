from langchain_core.prompts import ChatPromptTemplate


sap_optimization_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert SAP ABAP code optimization assistant.

Optimize the provided ABAP code using only the
retrieved optimization rules.

Important requirements:

- Preserve the original business logic.
- Preserve the expected functional behavior.
- Do not invent requirements.
- Do not invent company-specific rules.
- Apply the retrieved optimization rules.
- Improve performance where the rules justify the change.
- Avoid unnecessary database calls.
- Keep the resulting ABAP readable and maintainable.
- Return the complete optimized ABAP code.
"""
        ),
        (
            "human",
            """
Optimize the following SAP ABAP code.

Original Code:
{original_code}

Retrieved Optimization Rules:
{retrieved_context}

Return only the complete optimized ABAP code.
"""
        ),
    ]
)