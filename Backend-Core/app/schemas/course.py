from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.course import CourseLevel, ModuleType

class ModuleSchema(BaseModel):
    id: str
    type: ModuleType
    title: str
    duration: str
    completed: bool
    score: Optional[float] = None
    questions: Optional[int] = None
    pages: Optional[int] = None

class SectionSchema(BaseModel):
    id: str
    title: str
    completed: bool
    duration: str
    modules: List[ModuleSchema]

class InstructorSchema(BaseModel):
    id: str
    name: str

class CourseBase(BaseModel):
    title: str
    description: str
    duration: str
    category: str
    level: CourseLevel
    image: str

class CourseCreate(CourseBase):
    sections: List[SectionSchema]

class CourseListItem(BaseModel):
    id: str
    title: str
    description: str
    duration: str
    category: str
    level: str
    enrolled: bool
    rating: float
    image: str
    progress: float = 0.0

class CourseList(BaseModel):
    courses: List[CourseListItem]

class CourseDetail(CourseBase):
    id: str
    instructor: InstructorSchema
    rating: float
    enrollmentDate: Optional[datetime] = None
    progress: float = 0.0
    sections: List[SectionSchema]