from langgraph.graph import StateGraph, START, END

from app.models.graph_state import GenerationState
from app.services.llm_service import get_llm


def generate_response(state: GenerationState):
    llm = get_llm()

    response = llm.invoke(state["user_input"])

    return {
        "response": response.content
    }


def build_generation_graph():
    graph = StateGraph(GenerationState)

    graph.add_node("generate", generate_response)

    graph.add_edge(START, "generate")
    graph.add_edge("generate", END)

    return graph.compile()