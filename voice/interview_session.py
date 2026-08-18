"""
Voice Interview Session Engine
================================
Manages a full real-time AI voice interview session.

Flow per turn:
  start()  → generates opening question → TTS → returns audio path
  respond() → STT → evaluate → feedback → next question → TTS → returns audio path
"""

import asyncio
import uuid
import os

from voice.stt import speech_to_text
from voice.tts import text_to_speech
from ai.llm_adapter import generate_text_with_langchain


# ============================================================
# Config
# ============================================================

TECHNICAL_QUESTIONS = 15
PROJECT_QUESTIONS   = 10
HR_QUESTIONS        = 10
TOTAL_QUESTIONS     = TECHNICAL_QUESTIONS + PROJECT_QUESTIONS + HR_QUESTIONS

AUDIO_OUT_DIR = "data/audio_output/interview"

INTERVIEW_SYSTEM_PROMPT = """
You are a strict yet professional AI Interviewer conducting a real job interview.

CANDIDATE RESUME CONTEXT:
{resume_context}

INTERVIEW RULES:
- You are interviewing based on the candidate's resume above.
- Ask ONE question at a time.
- Keep each question clear and concise (1-2 sentences).
- Rotate across: Technical (skills-based), Project (project-based), HR (behavioral).
- Do NOT repeat questions already asked.
- After evaluating an answer, give brief spoken feedback (1 sentence) then ask the next question.
- Do NOT ask multiple questions at once.
- Do NOT break character.
- Keep everything conversational and spoken-friendly (no markdown, no bullet points, no special characters).
""".strip()


# ============================================================
# Interview Session
# ============================================================

class InterviewSession:

    def __init__(self, session_id: str, resume_text: str, skills: list, projects: list):
        self.session_id    = session_id
        self.resume_text   = resume_text
        self.skills        = skills
        self.projects      = projects
        self.history       = []          # list of {"role": "ai"|"user", "text": ...}
        self.question_num  = 0
        self.scores        = []
        self.done          = False

        # Build resume context summary for the prompt
        self.resume_context = self._build_resume_context()

        os.makedirs(AUDIO_OUT_DIR, exist_ok=True)


    def _build_resume_context(self) -> str:
        skills_str   = ", ".join(self.skills)   if self.skills   else "Not provided"
        projects_str = ", ".join(self.projects) if self.projects else "Not provided"
        return (
            f"Skills: {skills_str}\n"
            f"Projects: {projects_str}\n"
            f"Resume Text:\n{self.resume_text[:2000]}"  # limit to avoid token overflow
        )


    def _system_prompt(self) -> str:
        return INTERVIEW_SYSTEM_PROMPT.format(
            resume_context=self.resume_context
        )


    def _build_conversation_prompt(self, user_message: str = None) -> str:
        """Build the full conversation as a prompt string."""
        lines = []

        for turn in self.history:
            prefix = "Interviewer:" if turn["role"] == "ai" else "Candidate:"
            lines.append(f"{prefix} {turn['text']}")

        if user_message:
            lines.append(f"Candidate: {user_message}")

        # Instruct AI what to do next
        remaining = TOTAL_QUESTIONS - self.question_num
        if remaining <= 0:
            lines.append(
                "Interviewer: [The interview is complete. Give a warm closing statement "
                "and tell the candidate they will receive feedback shortly. "
                "Do NOT ask any more questions.]"
            )
        else:
            q_type = self._next_question_type()
            lines.append(
                f"Interviewer: [Now ask ONE {q_type} interview question "
                f"based on the candidate's resume. "
                f"This is question {self.question_num + 1} of {TOTAL_QUESTIONS}.]"
            )

        return "\n".join(lines)


    def _next_question_type(self) -> str:
        """Cycle: technical (first 15), project (next 10), HR (last 10)."""
        n = self.question_num
        if n < TECHNICAL_QUESTIONS:
            return "technical"
        elif n < TECHNICAL_QUESTIONS + PROJECT_QUESTIONS:
            return "project-based"
        else:
            return "HR / behavioral"


    async def _speak(self, text: str) -> str:
        """Convert text to speech and return the audio file path."""
        audio_path = os.path.join(
            AUDIO_OUT_DIR,
            f"{self.session_id}_q{self.question_num}.mp3"
        )
        await text_to_speech(text, audio_path)
        return audio_path


    async def start(self) -> dict:
        """
        Begin the interview. Generate and speak the opening + first question.
        Returns: { question_num, question_text, audio_path, done }
        """
        opening_prompt = (
            f"Interviewer: [Start the interview. Greet the candidate warmly, "
            f"introduce yourself as the AI interviewer, and then immediately ask "
            f"the first technical question about their skills: "
            f"{', '.join(self.skills[:3]) or 'their background'}. "
            f"Keep it natural and spoken-friendly. No markdown. "
            f"One greeting + one question only.]"
        )

        question_text = await asyncio.to_thread(
            generate_text_with_langchain,
            prompt=opening_prompt,
            system_prompt=self._system_prompt()
        )

        self.history.append({"role": "ai", "text": question_text})
        self.question_num += 1

        audio_path = await self._speak(question_text)

        return {
            "session_id":    self.session_id,
            "question_num":  self.question_num,
            "total":         TOTAL_QUESTIONS,
            "question_text": question_text,
            "audio_path":    audio_path,
            "done":          False,
        }


    async def respond(self, audio_path: str) -> dict:
        """
        Process the user's audio answer.
        Returns: { transcript, feedback, score, next_question, audio_path, done }
        """
        # ---- STT ----
        transcript = await speech_to_text(audio_path)
        self.history.append({"role": "user", "text": transcript})

        # ---- Check if interview is over ----
        if self.question_num >= TOTAL_QUESTIONS:
            closing_prompt = (
                "Interviewer: [The interview is now complete. "
                "Give a warm, encouraging closing statement in 2 sentences. "
                "Do NOT ask any more questions. No markdown.]"
            )
            closing_text = await asyncio.to_thread(
                generate_text_with_langchain,
                prompt="\n".join(
                    f"{'Interviewer' if t['role']=='ai' else 'Candidate'}: {t['text']}"
                    for t in self.history
                ) + f"\n{closing_prompt}",
                system_prompt=self._system_prompt()
            )
            audio_out = await self._speak(closing_text)
            self.done = True
            avg_score = round(sum(self.scores) / len(self.scores), 1) if self.scores else 0
            return {
                "transcript":    transcript,
                "feedback":      closing_text,
                "score":         None,
                "next_question": None,
                "audio_path":    audio_out,
                "done":          True,
                "average_score": avg_score,
                "history":       self.history,
            }

        # ---- Evaluate answer + ask next question ----
        eval_prompt = self._build_conversation_prompt(user_message=None)

        eval_instruction = (
            f"The candidate just answered: '{transcript}'\n\n"
            f"Evaluate their answer in 1 brief spoken sentence (mention a score out of 10), "
            f"then immediately ask the next {self._next_question_type()} question. "
            f"Keep it natural, no markdown, no bullet points."
        )

        full_prompt = eval_prompt + "\n\n" + eval_instruction

        response_text = await asyncio.to_thread(
            generate_text_with_langchain,
            prompt=full_prompt,
            system_prompt=self._system_prompt()
        )

        # Extract score from text (best-effort)
        score = self._extract_score(response_text)
        self.scores.append(score)

        self.history.append({"role": "ai", "text": response_text})
        self.question_num += 1

        audio_out = await self._speak(response_text)

        return {
            "transcript":    transcript,
            "feedback":      response_text,
            "score":         score,
            "next_question": response_text,
            "audio_path":    audio_out,
            "done":          False,
            "question_num":  self.question_num,
            "total":         TOTAL_QUESTIONS,
        }


    def _extract_score(self, text: str) -> int:
        """Try to extract a numeric score like '7/10' or '8 out of 10' from text."""
        import re
        match = re.search(r"(\d+)\s*/\s*10", text)
        if match:
            return min(int(match.group(1)), 10)
        match = re.search(r"(\d+)\s+out\s+of\s+10", text)
        if match:
            return min(int(match.group(1)), 10)
        return 7  # default if not parseable


    def get_summary(self) -> dict:
        avg = round(sum(self.scores) / len(self.scores), 1) if self.scores else 0
        return {
            "session_id":     self.session_id,
            "total_questions": TOTAL_QUESTIONS,
            "answered":        len([t for t in self.history if t["role"] == "user"]),
            "average_score":   avg,
            "scores":          self.scores,
            "history":         self.history,
            "done":            self.done,
        }


# ============================================================
# In-memory session store
# ============================================================

_sessions: dict[str, InterviewSession] = {}


def create_interview_session(resume_text: str, skills: list, projects: list) -> str:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = InterviewSession(session_id, resume_text, skills, projects)
    return session_id


def get_interview_session(session_id: str) -> InterviewSession | None:
    return _sessions.get(session_id)
