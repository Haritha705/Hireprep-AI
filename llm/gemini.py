from ai.llm_adapter import generate_text_with_langchain


def ask_gemini(prompt: str):
    """Generate a response through the shared LangChain adapter."""
    return generate_text_with_langchain(prompt, system_prompt="You are a helpful assistant.")