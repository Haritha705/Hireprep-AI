import uuid
from datetime import datetime


class SessionService:

    def __init__(self):
        self.sessions = {}

    def create_session(self, resume_context: str):
        """
        Create a new interview session.
        """
        session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "resume_context": resume_context,
            "questions": [],
            "answers": [],
            "evaluations": [],
            "current_question": None,
            "completed": False
        }

        return session_id

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)

    def add_question(self, session_id: str, question: str):
        if session_id in self.sessions:
            self.sessions[session_id]["questions"].append(question)
            self.sessions[session_id]["current_question"] = question

    def add_answer(self, session_id: str, answer: str):
        if session_id in self.sessions:
            self.sessions[session_id]["answers"].append(answer)

    def add_evaluation(self, session_id: str, evaluation: dict):
        if session_id in self.sessions:
            self.sessions[session_id]["evaluations"].append(evaluation)

    def finish_session(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id]["completed"] = True

    def session_summary(self, session_id: str):

        session = self.sessions.get(session_id)

        if not session:
            return None

        evaluations = session["evaluations"]

        if len(evaluations) == 0:
            average = 0
        else:
            average = sum(
                e.get("overall_score", 0)
                for e in evaluations
            ) / len(evaluations)

        return {
            "session_id": session_id,
            "questions_answered": len(session["answers"]),
            "average_score": round(average, 2),
            "completed": session["completed"]
        }


# Singleton instance
session_manager = SessionService()