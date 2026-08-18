from fastapi import APIRouter
from pydantic import BaseModel

from llm.evaluator import InterviewEvaluator
from llm.feedback import FeedbackGenerator


router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

class EvaluationRequest(BaseModel):
    question: str
    answer: str
    resume_context: str = ""

@router.post("")
async def evaluate(request: EvaluationRequest):
    evaluation = InterviewEvaluator.evaluate(
        question=request.question,
        answer=request.answer,
        resume_context=request.resume_context
    )
    feedback = FeedbackGenerator.generate(
        question=request.question,
        answer=request.answer,
        evaluation=evaluation
    )
    return {
        "evaluation": evaluation,
        "feedback": feedback
    }
