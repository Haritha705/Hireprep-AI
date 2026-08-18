from fastapi import APIRouter
from pydantic import BaseModel

from services.interview_service import generate_questions


router = APIRouter(prefix="/interview", tags=["Interview"])

class InterviewRequest(BaseModel):
    skills: str
    projects: str = ""

@router.post("")
async def interview(request: InterviewRequest):
    skill_list = [item.strip() for item in request.skills.split(",") if item.strip()]
    project_list = [item.strip() for item in request.projects.split(",") if item.strip()]
    result = await generate_questions(skill_list, project_list)
    return result
