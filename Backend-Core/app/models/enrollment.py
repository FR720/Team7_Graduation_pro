from datetime import datetime
from typing import Dict, Optional
from beanie import Document

class Enrollment(Document):
    user_id: str
    course_id: str
    enrollment_date: datetime = datetime.utcnow()
    progress: float = 0.0
    module_progress: Dict[str, bool] = {}
    module_scores: Dict[str, float] = {}
    last_activity: Optional[datetime] = None

    class Settings:
        name = "enrollments"