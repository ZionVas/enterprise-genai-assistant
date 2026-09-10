from langgraph.graph import StateGraph, START, END

from app.models.sap_naming_state import SAPNamingState
from app.prompts.sap_naming_prompts import sap_naming_prompt
from app.services.llm_service import get_llm
from app.rag.reranked_retriever import retrieve_with_reranking


def retrieve_naming_rules(state: SAPNamingState):

    query = (
        "SAP ABAP naming conventions for variables, "
        "internal tables, structures, work areas and constants. "
        "Identify rules relevant to the following code:\n\n"
        + state["original_code"]
    )

    results = retrieve_with_reranking(
        query=query,
        top_k=5,
        retrieval_k=10,
    )

    context_parts = []
    sources = []

    for result in results:

        metadata = result.get(
            "metadata",
            {},
        )

        context_parts.append(
            f"""
Source: {metadata.get("document_name", "Unknown")}
Category: {metadata.get("category", "Unknown")}

Rule:
{result["text"]}
""".strip()
        )

        sources.append(
            {
                "document_name": metadata.get(
                    "document_name",
                    "Unknown",
                ),
                "category": metadata.get(
                    "category",
                    "Unknown",
                ),
                "page": metadata.get("page"),
                "chunk_id": result.get("chunk_id"),
                "reranker_score": result.get(
                    "reranker_score"
                ),
            }
        )

    retrieved_context = "\n\n---\n\n".join(
        context_parts
    )

    return {
        "retrieved_context": retrieved_context,
        "sources": sources,
    }


def correct_naming(state: SAPNamingState):

    llm = get_llm()

    prompt = sap_naming_prompt.invoke(
        {
            "original_code": state["original_code"],
            "retrieved_context": state[
                "retrieved_context"
            ],
        }
    )

    response = llm.invoke(prompt)

    return {
        "corrected_code": response.content
    }


def build_sap_naming_graph():

    graph = StateGraph(
        SAPNamingState
    )

    graph.add_node(
        "retrieve_naming_rules",
        retrieve_naming_rules,
    )

    graph.add_node(
        "correct_naming",
        correct_naming,
    )

    graph.add_edge(
        START,
        "retrieve_naming_rules",
    )

    graph.add_edge(
        "retrieve_naming_rules",
        "correct_naming",
    )

    graph.add_edge(
        "correct_naming",
        END,
    )

    return graph.compile()