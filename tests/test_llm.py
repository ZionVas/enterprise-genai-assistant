from app.services.generation_graph import build_generation_graph


def main():
    graph = build_generation_graph()

    result = graph.invoke(
        {
            "user_input": "Explain RAG in simple terms.",
            "response": "",
        }
    )

    print("\nGenerated response:\n")
    print(result["response"])


if __name__ == "__main__":
    main()