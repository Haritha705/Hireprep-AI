from typing import Any

from langchain_core.tools import tool

from parser.resume_parser import parse_resume


@tool
def resume_tool(resume_text: str) -> dict[str, Any]:
    """Parse resume text and return extracted skills and projects using the existing parser module."""
    try:
        result = parse_resume(resume_text)
        return {
            "status": "success",
            "data": result,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": f"Resume parsing failed: {exc}",
        }
