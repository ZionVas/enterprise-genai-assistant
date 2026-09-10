from langgraph.graph import StateGraph, START, END

from app.config import Config

from app.models.sap_optimization_state import SAPOptimizationState
from app.prompts.sap_optimization_prompts import sap_optimization_prompt
from app.prompts.sap_validation_prompts import sap_validation_prompt
from app.services.llm_service import get_llm
from app.rag.reranked_retriever import retrieve_with_reranking

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.models.sap_optimization_state import (
    SAPOptimizationState,
)

from app.prompts.sap_optimization_prompts import (
    sap_optimization_prompt,
)

from app.prompts.sap_validation_prompts import (
    sap_validation_prompt,
)

from app.services.llm_service import get_llm

from app.rag.reranked_retriever import (
    retrieve_with_reranking,
)


MAX_ITERATIONS = Config.MAX_OPTIMIZATION_ITERATIONS


def retrieve_optimization_rules(
    state: SAPOptimizationState,
):

    query = (
        "SAP ABAP code optimization rules "
        "for performance, database access, "
        "SELECT statements, loops and internal tables.\n\n"
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
Source:
{metadata.get("document_name", "Unknown")}

Category:
{metadata.get("category", "Unknown")}

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
                "page": metadata.get(
                    "page"
                ),
                "chunk_id": result.get(
                    "chunk_id"
                ),
                "reranker_score": result.get(
                    "reranker_score"
                ),
            }
        )

    return {
        "retrieved_context":
            "\n\n---\n\n".join(
                context_parts
            ),
        "sources": sources,
    }


def optimize_code(
    state: SAPOptimizationState,
):

    llm = get_llm()

    prompt = sap_optimization_prompt.invoke(
        {
            "original_code":
                state["original_code"],

            "retrieved_context":
                state["retrieved_context"],
        }
    )

    response = llm.invoke(prompt)

    return {
        "optimized_code":
            response.content,

        "iteration":
            state["iteration"] + 1,
    }


def validate_code(
    state: SAPOptimizationState,
):

    llm = get_llm()

    prompt = sap_validation_prompt.invoke(
        {
            "original_code":
                state["original_code"],

            "optimized_code":
                state["optimized_code"],

            "retrieved_context":
                state["retrieved_context"],
        }
    )

    response = llm.invoke(prompt)

    validation_result = response.content.strip()

    if validation_result.startswith("PASS"):

        return {
            "validation_passed": True,
            "validation_errors": [],
        }

    return {
        "validation_passed": False,
        "validation_errors": [
            validation_result
        ],
    }


def repair_code(
    state: SAPOptimizationState,
):

    llm = get_llm()

    repair_prompt = f"""
You are an SAP ABAP optimization repair assistant.

The previous optimization did not pass validation.

Original ABAP:
{state["original_code"]}

Current optimized ABAP:
{state["optimized_code"]}

Optimization rules:
{state["retrieved_context"]}

Validation problems:
{chr(10).join(state["validation_errors"])}

Repair the optimized ABAP.

Requirements:

- Preserve business logic.
- Fix the validation problems.
- Follow the optimization rules.
- Return only the complete corrected ABAP code.
"""

    response = llm.invoke(
        repair_prompt
    )

    return {
        "optimized_code":
            response.content,

        "iteration":
            state["iteration"] + 1,
    }


def route_after_validation(
    state: SAPOptimizationState,
):

    if state["validation_passed"]:

        return "finish"

    if state["iteration"] >= MAX_ITERATIONS:

        return "finish"

    return "repair"


def build_sap_optimization_graph():

    graph = StateGraph(
        SAPOptimizationState
    )

    graph.add_node(
        "retrieve_optimization_rules",
        retrieve_optimization_rules,
    )

    graph.add_node(
        "optimize_code",
        optimize_code,
    )

    graph.add_node(
        "validate_code",
        validate_code,
    )

    graph.add_node(
        "repair_code",
        repair_code,
    )

    graph.add_edge(
        START,
        "retrieve_optimization_rules",
    )

    graph.add_edge(
        "retrieve_optimization_rules",
        "optimize_code",
    )

    graph.add_edge(
        "optimize_code",
        "validate_code",
    )

    graph.add_conditional_edges(
        "validate_code",
        route_after_validation,
        {
            "repair":
                "repair_code",

            "finish":
                END,
        },
    )

    graph.add_edge(
        "repair_code",
        "validate_code",
    )

    return graph.compile()