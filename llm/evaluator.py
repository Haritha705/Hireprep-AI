import json
class InterviewEvaluator:

    @staticmethod
    def evaluate(
        question: str,
        answer: str,
        resume_context: str = ""
    ) -> dict:

        prompt = f"""
You are an expert AI Interview Evaluator.

Candidate Resume:
{resume_context}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return ONLY valid JSON.

Format:

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
- Be fair and objective.
- Do not return markdown.
- Return only JSON.
"""

        from ai.llm_adapter import generate_text_with_langchain
        
        content = generate_text_with_langchain(
            prompt=prompt,
            system_prompt="You are an expert interview evaluator."
        )

        # Remove markdown if present
        if content.startswith("```"):
            content = (
                content.replace("```json", "")
                       .replace("```", "")
                       .strip()
            )

        try:
            return json.loads(content)

        except json.JSONDecodeError:
            return {
                "technical_score": 0,
                "communication_score": 0,
                "confidence_score": 0,
                "overall_score": 0,
                "strengths": [],
                "weaknesses": [],
                "missing_points": [],
                "feedback": content
            }