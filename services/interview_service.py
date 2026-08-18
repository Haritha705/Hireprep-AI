from role_detector.detector import detect_role
from vectordb.retriever import get_interview_questions
from llm.fallback import generate_response


async def generate_questions(skills, projects=None):

    # --------------------------------------------------
    # Step 0: Normalize Input
    # --------------------------------------------------
    skills = skills or []
    projects = projects or []

    # Make sure everything is a string
    skills = [str(skill).strip() for skill in skills if skill]
    projects = [str(project).strip() for project in projects if project]

    # --------------------------------------------------
    # Step 1: Detect Candidate Role
    # --------------------------------------------------
    role = detect_role(skills)

    # --------------------------------------------------
    # Step 2: Build Semantic Search Query
    # --------------------------------------------------
    query_parts = skills + projects
    query = " ".join(query_parts).strip()

    # Fallback query if no skills/projects are available
    if not query:
        query = role

    # --------------------------------------------------
    # Step 3: Retrieve Questions using RAG
    # --------------------------------------------------
    questions = await get_interview_questions(
        query=query,
        resume_role=role
    )

    # --------------------------------------------------
    # Step 4: Safely Extract Retrieved Questions
    # --------------------------------------------------
    technical_questions = questions.get("technical", [])
    hr_questions = questions.get("hr", [])
    project_questions = questions.get("project", [])

    # --------------------------------------------------
    # Step 5: Build Prompt for Gemini/Groq
    # --------------------------------------------------
    prompt = f"""
You are an expert AI Interview Coach.

Analyze the candidate information and the retrieved interview questions.

Candidate Role:
{role}

Candidate Skills:
{', '.join(skills) if skills else "Not provided"}

Candidate Projects:
{', '.join(projects) if projects else "Not provided"}

Retrieved Technical Questions:
{technical_questions}

Retrieved HR Questions:
{hr_questions}

Retrieved Project Questions:
{project_questions}

Generate a professional interview preparation guide.

IMPORTANT RULES:

- Use proper Markdown formatting.
- Do NOT write long paragraphs.
- Use headings.
- Use numbered sections.
- Use bullet points.
- Keep every point concise.
- Maximum 400 words.
- Personalize the guide according to the candidate's role, skills,
  projects, and retrieved questions.
- Do not invent skills or projects that are not provided.

Return EXACTLY in the following format:

# Interview Preparation Guide

## 1. Key Skills to Revise
- Skill 1
- Skill 2
- Skill 3

## 2. Important Technical Topics
- Topic 1
- Topic 2
- Topic 3

## 3. HR Interview Tips
- Tip 1
- Tip 2
- Tip 3

## 4. Project Discussion Tips
- Explain project architecture
- Mention your role
- Explain challenges faced
- Explain solutions implemented

## 5. Common Mistakes to Avoid
- Mistake 1
- Mistake 2
- Mistake 3

## 6. Final Interview Tips
- Tip 1
- Tip 2
- Tip 3

Return ONLY the interview preparation guide.
"""

    # --------------------------------------------------
    # Step 6: Generate AI Response
    # --------------------------------------------------
    llm_response = generate_response(prompt)

    # --------------------------------------------------
    # Step 7: Return Final Response
    # --------------------------------------------------
    return {
        "detected_role": role,

        "technical_questions": technical_questions,

        "hr_questions": hr_questions,

        "project_questions": project_questions,

        "ai_interview_guide": {
            "model": llm_response.get("model"),
            "response": llm_response.get("response")
        }
    }