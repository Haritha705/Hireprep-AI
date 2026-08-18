from parser.skill_parser import extract_skills
from parser.project_parser import extract_projects


def parse_resume(resume_text):

    return {
        "skills": extract_skills(resume_text),
        "projects": extract_projects(resume_text)
    }