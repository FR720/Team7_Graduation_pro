from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ActivityDay(BaseModel):
    day: str
    hours: float

class EnrollmentResponse(BaseModel):
    success: bool
    enrollment_id: str
    enrollment_date: datetime

class ModuleProgressUpdate(BaseModel):
    completed: bool
    score: Optional[float] = None

class ModuleProgressResponse(BaseModel):
    success: bool
    course_progress: float

class UserActivityResponse(BaseModel):
    activity: List[ActivityDay]