from langchain_core.prompts import ChatPromptTemplate


email_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an enterprise email writing assistant.

Write clear, professional and natural emails.

Follow these requirements:
- Do not invent facts.
- Use only the information provided by the user.
- Maintain the requested tone.
- Keep the email concise and easy to read.
- Include an appropriate greeting.
- Include an appropriate closing.
"""
        ),
        (
            "human",
            """
Create an email using the following information.

Recipient:
{recipient}

Purpose:
{purpose}

Key Points:
{key_points}

Tone:
{tone}

Length:
{length}

Return only the email body.
"""
        ),
    ]
)