from litellm import completion
import config

from services.session_service import session_manager


class ReportService:

    @staticmethod
    def generate_report(session_id: str):

        session = session_manager.get_session(session_id)

        if not session:
            return {
                "error": "Session not found"
            }

        evaluations = session["evaluations"]

        if len(evaluations) == 0:
            return {
                "error": "No interview data available."
            }

        avg_technical = round(
            sum(e.get("technical_score", 0) for e in evaluations) / len(evaluations),
            2
        )

        avg_communication = round(
            sum(e.get("communication_score", 0) for e in evaluations) / len(evaluations),
            2
        )

        avg_confidence = round(
            sum(e.get("confidence_score", 0) for e in evaluations) / len(evaluations),
            2
        )

        avg_overall = round(
            sum(e.get("overall_score", 0) for e in evaluations) / len(evaluations),
            2
        )

        prompt = f"""
You are an expert interview coach.

Generate a professional interview report.

Average Technical Score: {avg_technical}/10
Average Communication Score: {avg_communication}/10
Average Confidence Score: {avg_confidence}/10
Overall Score: {avg_overall}/10

Evaluation Details:
{evaluations}

Generate a report with these sections:

1. Overall Performance
2. Technical Skills
3. Communication Skills
4. Confidence Level
5. Strengths
6. Areas for Improvement
7. Recommended Learning Path
8. Final Verdict

Keep it concise and professional.
"""

        response = completion(
            model=f"gemini/{config.GEMINI_MODEL}",
            api_key=config.GEMINI_API_KEY,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional interview evaluator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        report = response.choices[0].message.content

        return {
            "session_id": session_id,
            "questions_answered": len(session["questions"]),
            "technical_score": avg_technical,
            "communication_score": avg_communication,
            "confidence_score": avg_confidence,
            "overall_score": avg_overall,
            "report": report
        }