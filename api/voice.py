import os
import shutil

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from voice.assistant import VoiceAssistant
from voice.interview_session import (
    create_interview_session,
    get_interview_session,
)
from parser.pdf_parser import extract_resume_text
from parser.resume_parser import parse_resume

router = APIRouter(prefix="/voice", tags=["Voice"])
assistant = VoiceAssistant()


# ============================================================
# Existing: generic voice chat
# ============================================================

@router.post("")
async def voice_chat(audio: UploadFile = File(...)):
    save_path = f"data/recordings/{audio.filename}"
    os.makedirs("data/recordings", exist_ok=True)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    result = await assistant.converse(save_path)
    return {"response": result}


# ============================================================
# NEW: Start a voice interview session
# POST /voice/interview/start
#   - resume: UploadFile (PDF)  OR  resume_text: str (Form field)
#   - Returns: session_id, first question text, audio URL
# ============================================================

@router.post("/interview/start")
async def start_interview(
    resume: UploadFile = File(None),
    resume_text: str   = Form(None),
):
    # ---- Get resume text ----
    if resume is not None:
        save_path = f"data/resume/{resume.filename}"
        os.makedirs("data/resume", exist_ok=True)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        raw_text = extract_resume_text(save_path)
    elif resume_text:
        raw_text = resume_text
    else:
        raise HTTPException(
            status_code=400,
            detail="Provide either a resume PDF file or resume_text."
        )

    # ---- Parse skills & projects ----
    parsed = parse_resume(raw_text)
    skills   = parsed.get("skills", [])
    projects = parsed.get("projects", [])

    # ---- Create session ----
    session_id = create_interview_session(raw_text, skills, projects)
    session    = get_interview_session(session_id)

    # ---- Start interview (generate + TTS first question) ----
    result = await session.start()

    return {
        "session_id":    session_id,
        "question_num":  result["question_num"],
        "total":         result["total"],
        "question_text": result["question_text"],
        "audio_url":     f"/voice/interview/audio/{session_id}/{os.path.basename(result['audio_path'])}",
        "done":          False,
    }


# ============================================================
# NEW: Submit voice answer and get next question
# POST /voice/interview/respond
#   - session_id: str (Form)
#   - audio: UploadFile (WAV/MP3 of user's spoken answer)
#   - Returns: transcript, feedback, score, next question audio URL
# ============================================================

@router.post("/interview/respond")
async def respond_to_interview(
    session_id: str    = Form(...),
    audio: UploadFile  = File(...),
):
    session = get_interview_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Please start a new interview.")

    if session.done:
        raise HTTPException(status_code=400, detail="Interview is already completed.")

    # ---- Save audio ----
    os.makedirs("data/recordings/interview", exist_ok=True)
    save_path = f"data/recordings/interview/{session_id}_{audio.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # ---- Process response ----
    result = await session.respond(save_path)

    audio_filename = os.path.basename(result["audio_path"])

    return {
        "session_id":    session_id,
        "transcript":    result["transcript"],
        "feedback":      result["feedback"],
        "score":         result["score"],
        "audio_url":     f"/voice/interview/audio/{session_id}/{audio_filename}",
        "done":          result["done"],
        "question_num":  result.get("question_num"),
        "total":         result.get("total"),
        "average_score": result.get("average_score"),
    }


# ============================================================
# NEW: Get session summary
# GET /voice/interview/summary/{session_id}
# ============================================================

@router.get("/interview/summary/{session_id}")
async def interview_summary(session_id: str):
    session = get_interview_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session.get_summary()


# ============================================================
# Serve generated interview audio files
# GET /voice/interview/audio/{session_id}/{filename}
# ============================================================

@router.get("/interview/audio/{session_id}/{filename}")
async def serve_interview_audio(session_id: str, filename: str):
    file_path = os.path.join("data/audio_output/interview", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")
    return FileResponse(file_path, media_type="audio/mpeg")