from langchain_core.prompts import ChatPromptTemplate


sap_naming_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP ABAP naming convention assistant.

Your task is to correct naming convention violations
in the provided ABAP code.

Important requirements:

- Preserve the original program logic.
- Do not change business logic.
- Do not change SQL statements unless required for naming correction.
- Do not add new functionality.
- Apply only the retrieved SAP naming convention rules.
- Do not invent company-specific naming rules.
- Preserve valid existing names when they already follow the rules.
- Return the complete corrected ABAP code.
"""
        ),
        (
            "human",
            """
Correct the naming conventions in the following SAP ABAP code.

Original ABAP Code:
{original_code}

Retrieved SAP Naming Rules:
{retrieved_context}

Return only the complete corrected ABAP code.
"""
        ),
    ]
)