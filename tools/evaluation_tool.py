from typing import Any

from langchain_core.tools import tool

from llm.evaluator import InterviewEvaluator
from llm.feedback import FeedbackGenerator


@tool
def evaluation_tool(question: str, answer: str, resume_context: str = "") -> dict[str, Any]:
    """Evaluate a candidate answer and return structured feedback using existing evaluation modules."""
    try:
        evaluation = InterviewEvaluator.evaluate(question=question, answer=answer, resume_context=resume_context)
        feedback = FeedbackGenerator.generate(question=question, answer=answer, evaluation=evaluation)
        return {
            "status": "success",
            "data": {
                "evaluation": evaluation,
                "feedback": feedback,
            },
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": f"Evaluation failed: {exc}",
        }
