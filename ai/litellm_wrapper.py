from ai.llm_adapter import generate_text_with_langchain


def generate_text(prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
    """Thin wrapper around the shared LangChain-backed response path."""
    return generate_text_with_langchain(prompt, system_prompt=system_prompt)
