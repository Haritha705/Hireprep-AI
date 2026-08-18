class FeedbackGenerator:

    @staticmethod
    def generate(
        question: str,
        answer: str,
        evaluation: dict
    ) -> str:

        prompt = f"""
You are an experienced interview coach.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluation Results:
Technical Score: {evaluation.get("technical_score")}
Communication Score: {evaluation.get("communication_score")}
Confidence Score: {evaluation.get("confidence_score")}
Overall Score: {evaluation.get("overall_score")}

Strengths:
{evaluation.get("strengths")}

Weaknesses:
{evaluation.get("weaknesses")}

Missing Points:
{evaluation.get("missing_points")}

Generate feedback with the following format:

1. Appreciation (1 sentence)
2. What was done well
3. What should be improved
4. Tips for the next interview question

Keep it under 120 words.
"""

        from ai.llm_adapter import generate_text_with_langchain
        
        content = generate_text_with_langchain(
            prompt=prompt,
            system_prompt="You are a professional interview mentor."
        )

        return content