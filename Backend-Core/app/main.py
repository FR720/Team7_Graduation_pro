from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.chat import ChatMessage
from app.auth.auth import router as auth_router
from app.routes.courses import router as courses_router
from app.routes.users import router as users_router
from app.routes.chat import router as chat_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(chat_router, prefix="/courses", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    try:
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[
                User,
                Course,
                Enrollment,
                ChatMessage
            ]
        )
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "Course Platform API"}