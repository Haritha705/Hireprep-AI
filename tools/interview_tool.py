import json
from typing import Any

from langchain_core.tools import tool

from services.interview_service import generate_questions


@tool
async def interview_tool(skills: str, projects: str = "") -> dict[str, Any]:
    """Generate interview prep guidance by delegating to the existing interview service."""
    try:
        skill_list = [item.strip() for item in skills.split(",") if item.strip()]
        project_list = [item.strip() for item in projects.split(",") if item.strip()]
        result = await generate_questions(skill_list, project_list)
        return {
            "status": "success",
            "data": result,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": f"Interview generation failed: {exc}",
        }
