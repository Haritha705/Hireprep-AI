from services.interview_service import generate_questions

from fastapi import APIRouter, UploadFile, File
import os
import shutil
import traceback

from parser.pdf_parser import extract_resume_text
from parser.resume_parser import parse_resume

router = APIRouter()

UPLOAD_FOLDER = "data/resume"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    try:

        print("\n===== STEP 1 : Saving Resume =====")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("Resume Saved")

        print("\n===== STEP 2 : Extracting Text =====")

        resume_text = extract_resume_text(file_path)

        print("Text Extracted")

        print("\n===== STEP 3 : Parsing Resume =====")

        resume_data = parse_resume(resume_text)

        print(resume_data)

        print("\n===== STEP 4 : Generating Questions =====")

        questions = await generate_questions(
            skills=resume_data["skills"],
            projects=resume_data["projects"]
        )

        print("Questions Generated Successfully")

        return {
            "message": "Resume uploaded and interview generated successfully!",
            "filename": file.filename,
            "resume": resume_data,
            "questions": questions
        }

    except Exception as e:

        print("\n=========== ERROR ===========")
        traceback.print_exc()
        print("=============================\n")

        raise e