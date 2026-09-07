from langgraph.graph import StateGraph, START, END

from app.models.email_state import EmailState
from app.prompts.email_prompts import email_prompt
from app.services.llm_service import get_llm


def generate_email(state: EmailState):

    llm = get_llm()

    prompt = email_prompt.invoke(
        {
            "recipient": state["recipient"],
            "purpose": state["purpose"],
            "key_points": state["key_points"],
            "tone": state["tone"],
            "length": state["length"],
        }
    )

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


def build_email_graph():

    graph = StateGraph(EmailState)

    graph.add_node("generate_email", generate_email)

    graph.add_edge(START, "generate_email")
    graph.add_edge("generate_email", END)

    return graph.compile()