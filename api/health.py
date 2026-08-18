from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    return {
        "status": "Healthy",
        "backend": "Running",
        "message": "AI Resume Interview Preparation API is working."
    }