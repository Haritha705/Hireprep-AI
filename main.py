# -----------------------------
# Imports
# -----------------------------

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from db.Mongodb import connect_to_mongo, close_mongo_connection
from api.health import router as health_router
from api.upload import router as upload_router
from api.chatbot import router as chatbot_router
from api.voice import router as voice_router
from api.evaluation import router as evaluation_router
from api.interview import router as interview_router
from api.auth import router as auth_router


# -----------------------------
# Lifespan (Startup / Shutdown)
# -----------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


# -----------------------------
# Create FastAPI App
# -----------------------------
app = FastAPI(
    title="HirePrep AI",
    version="2.0.0",
    description="AI Resume Interview Preparation Platform with RAG, Voice Assistant, and AI Evaluation",
    lifespan=lifespan
)


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
async def root():
    return {
        "message": "HirePrep AI Backend is running",
        "status": "success",
        "docs": "/docs"
    }


# -----------------------------
# Enable CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Register Routers
# -----------------------------

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chatbot_router)
app.include_router(voice_router)
app.include_router(evaluation_router)
app.include_router(interview_router)
app.include_router(auth_router)


# -----------------------------
# Static Files (Voice Interview UI)
# -----------------------------
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")