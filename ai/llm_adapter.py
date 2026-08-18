from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from config import GEMINI_API_KEY, GEMINI_MODEL, GROQ_MODEL
import os


def build_gemini():
    if not GEMINI_API_KEY:
        return None

    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.2,
    )


def build_groq():
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        return None

    return ChatGroq(
        model=GROQ_MODEL,
        groq_api_key=groq_api_key,
        temperature=0.2,
    )


def build_llm():
    """
    Return Gemini as the primary LangChain chat model.
    The agent can fall back to Groq when Gemini fails.
    """
    llm = build_gemini()

    if llm is not None:
        return llm

    return build_groq()


def get_fallback_llm():
    return build_groq()


def generate_text_with_langchain(
    prompt: str,
    system_prompt: str = "You are a helpful assistant.",
) -> str:

    llm = build_llm()

    if llm is None:
        return "No LLM API key is configured."

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt),
        ])

        content = getattr(response, "content", None)

        if isinstance(content, list):
            texts = []

            for item in content:
                if isinstance(item, dict):
                    texts.append(str(item.get("text", "")))
                else:
                    texts.append(str(item))

            return "".join(texts).strip()

        return str(content).strip() if content else str(response)

    except Exception as exc:
        # Try real Groq fallback
        fallback = get_fallback_llm()

        if fallback is None:
            return f"LLM generation failed: {exc}"

        try:
            response = fallback.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=prompt),
            ])

            content = getattr(response, "content", None)

            return str(content).strip() if content else str(response)

        except Exception as fallback_exc:
            return (
                f"Primary LLM failed: {exc}. "
                f"Fallback LLM failed: {fallback_exc}"
            )