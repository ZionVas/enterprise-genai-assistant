from langgraph.graph import StateGraph, START, END

from app.models.code_state import CodeGenerationState
from app.prompts.code_prompts import code_generation_prompt
from app.services.llm_service import get_llm
from app.rag.reranked_retriever import retrieve_with_reranking # type: ignore


def retrieve_rules(state: CodeGenerationState):
    results = retrieve_with_reranking(
        query=state["user_request"],
        top_k=5,
        retrieval_k=10,
    )

    context_parts = []
    sources = []

    for result in results:
        metadata = result.get("metadata", {})

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
            }
        )

    retrieved_context = "\n\n---\n\n".join(
        context_parts
    )

    return {
        "retrieved_context": retrieved_context,
        "sources": sources,
    }


def generate_code(state: CodeGenerationState):
    llm = get_llm()

    prompt = code_generation_prompt.invoke(
        {
            "language": state["language"],
            "user_request": state["user_request"],
            "retrieved_context": state["retrieved_context"],
        }
    )

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


def build_code_generation_graph():
    graph = StateGraph(CodeGenerationState)

    graph.add_node(
        "retrieve_rules",
        retrieve_rules,
    )

    graph.add_node(
        "generate_code",
        generate_code,
    )

    graph.add_edge(
        START,
        "retrieve_rules",
    )

    graph.add_edge(
        "retrieve_rules",
        "generate_code",
    )

    graph.add_edge(
        "generate_code",
        END,
    )

    return graph.compile()