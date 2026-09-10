from langchain_ollama import ChatOllama

from app.config import Config


def get_llm():
    return ChatOllama(
        model=Config.LLM_MODEL,
        temperature=Config.LLM_TEMPERATURE,
    )