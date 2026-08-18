import re


def extract_projects(resume_text: str):

    projects = []

    lines = resume_text.split("\n")

    capture = False

    for line in lines:

        clean = line.strip()

        if clean.lower() == "projects":
            capture = True
            continue

        if capture:

            if clean == "":
                continue

            if clean.lower() in [
                "education",
                "experience",
                "skills",
                "certifications",
                "internship"
            ]:
                break

            projects.append(clean)

    return projects