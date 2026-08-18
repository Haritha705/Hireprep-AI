import time
import logging

from llm.gemini import ask_gemini
from llm.groq import ask_groq


logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2   # seconds

# Error messages that indicate a permanent failure (no point retrying)
_PERMANENT_ERROR_KEYWORDS = [
    "404",
    "not_found",
    "NOT_FOUND",
    "no longer available",
    "model_not_found",
    "does not exist",
]


def _is_permanent_error(exc: Exception) -> bool:
    """Return True if the exception indicates a permanent failure like 404."""
    msg = str(exc).lower()
    for keyword in _PERMANENT_ERROR_KEYWORDS:
        if keyword.lower() in msg:
            return True
    return False


def generate_response(prompt):
    start_time = time.time()
    gemini_error = None

    # --- Try Gemini (primary) ---
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = ask_gemini(prompt)
            end_time = time.time()
            return {
                "status": True,
                "model": "LangChain/Gemini",
                "response": response,
                "attempts": attempt,
                "response_time": round(end_time - start_time, 2),
            }
        except Exception as exc:
            gemini_error = exc
            logger.warning("Gemini attempt %d failed: %s", attempt, exc)

            # Don't retry permanent errors (e.g. 404 model not found)
            if _is_permanent_error(exc):
                logger.warning("Permanent Gemini error detected, skipping retries.")
                break

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    # --- Fallback to Groq ---
    logger.info("Falling back to Groq after Gemini failure.")
    try:
        response = ask_groq(prompt)
        end_time = time.time()
        return {
            "status": True,
            "model": "LangChain/Groq",
            "response": response,
            "attempts": MAX_RETRIES,
            "response_time": round(end_time - start_time, 2),
        }
    except Exception as groq_exc:
        end_time = time.time()
        logger.error("Both Gemini and Groq failed. Gemini: %s | Groq: %s", gemini_error, groq_exc)
        return {
            "status": False,
            "model": "None",
            "response": f"All LLM providers failed. Please try again later.",
            "attempts": MAX_RETRIES,
            "response_time": round(end_time - start_time, 2),
        }