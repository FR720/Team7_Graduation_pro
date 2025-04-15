from datetime import datetime
from typing import List, Optional
from beanie import Document
from pydantic import BaseModel
from enum import Enum

class CourseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ModuleType(str, Enum):
    VIDEO = "video"
    QUIZ = "quiz"
    READING = "reading"

class Module(BaseModel):
    id: str
    type: ModuleType
    title: str
    duration: str
    completed: bool = False
    score: Optional[float] = None
    questions: Optional[int] = None
    pages: Optional[int] = None

class Section(BaseModel):
    id: str
    title: str
    completed: bool = False
    duration: str
    modules: List[Module]

class Course(Document):
    title: str
    description: str
    duration: str
    category: str
    level: CourseLevel
    image: str
    rating: float = 0.0
    sections: List[Section]
    instructor_id: str

    class Settings:
        name = "courses"