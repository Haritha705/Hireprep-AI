"""
Centralized prompts for HirePrep AI.
All Gemini prompts should be defined here.
"""


class PromptTemplates:

    # -------------------------------
    # Interview Question Generator
    # -------------------------------
    INTERVIEW_SYSTEM = """
You are a professional AI Interviewer.

Rules:
- Ask one interview question at a time.
- Base questions on the candidate's resume.
- Start with easy questions and gradually increase difficulty.
- Be friendly and professional.
- Do not answer unrelated questions.
"""

    # -------------------------------
    # Resume Based Question Prompt
    # -------------------------------
    @staticmethod
    def interview_prompt(resume_context: str,
                         retrieved_context: str,
                         previous_questions: str = ""):

        return f"""
Candidate Resume:
{resume_context}

Relevant Interview Knowledge:
{retrieved_context}

Previous Questions:
{previous_questions}

Generate ONE interview question.

Requirements:
- Resume-specific
- Technical if applicable
- Medium difficulty
- Avoid repeating previous questions

Return ONLY the question.
"""

    # -------------------------------
    # Answer Evaluation Prompt
    # -------------------------------
    @staticmethod
    def evaluation_prompt(
        question: str,
        answer: str,
        resume_context: str
    ):

        return f"""
Candidate Resume:
{resume_context}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return ONLY valid JSON.

{{
    "technical_score": 0,
    "communication_score": 0,
    "confidence_score": 0,
    "overall_score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_points": [],
    "feedback": ""
}}

Rules:
- Scores should be between 0 and 10.
- Be objective.
- No markdown.
- Return only JSON.
"""

    # -------------------------------
    # Feedback Prompt
    # -------------------------------
    @staticmethod
    def feedback_prompt(
        question: str,
        answer: str,
        evaluation: dict
    ):

        return f"""
Interview Question:
{question}

Candidate Answer:
{answer}

Evaluation:
{evaluation}

Generate feedback.

Include:

1. Appreciation
2. Strengths
3. Improvements
4. Tips

Maximum 120 words.
"""

    # -------------------------------
    # Resume Summary Prompt
    # -------------------------------
    @staticmethod
    def resume_summary_prompt(resume_text: str):

        return f"""
Summarize the following resume.

Resume:

{resume_text}

Return:

- Candidate Name
- Role
- Skills
- Projects
- Experience
- Education

Keep it concise.
"""

    # -------------------------------
    # Speech Summary Prompt
    # -------------------------------
    @staticmethod
    def speech_summary_prompt(transcript: str):

        return f"""
Summarize this transcript in 2-3 concise sentences.

Transcript:

{transcript}
"""

    # -------------------------------
    # Final Interview Report
    # -------------------------------
    @staticmethod
    def final_report_prompt(interview_results: str):

        return f"""
Interview Results:

{interview_results}

Generate a professional interview report.

Include:

- Overall Performance
- Technical Skills
- Communication
- Confidence
- Strengths
- Weaknesses
- Recommended Topics
- Final Verdict

Keep it professional.
"""