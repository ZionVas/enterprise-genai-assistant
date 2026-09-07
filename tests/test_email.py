from app.services.email_graph import build_email_graph


def main():

    graph = build_email_graph()

    result = graph.invoke(
        {
            "recipient": "My manager",
            "purpose": "Request one day of leave",
            "key_points": "I need leave tomorrow due to a personal commitment.",
            "tone": "Professional",
            "length": "Short",
            "response": "",
        }
    )

    print("\nGenerated Email:\n")
    print(result["response"])


if __name__ == "__main__":
    main()