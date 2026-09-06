from langchain_ollama import ChatOllama


def get_llm():
    return ChatOllama(
        model="qwen3:4b",
        temperature=0.2,
    )