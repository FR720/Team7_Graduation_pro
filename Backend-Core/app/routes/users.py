from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.auth.auth import get_current_active_user
from app.models.user import User
from app.models.enrollment import Enrollment
from app.schemas.enrollment import UserActivityResponse, ActivityDay

router = APIRouter()

@router.get("/activity", response_model=UserActivityResponse)
async def get_user_activity(
    current_user: User = Depends(get_current_active_user),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    try:
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()

        enrollments = await Enrollment.find({
            "user_id": str(current_user.id),
            "last_activity": {"$gte": start_date, "$lte": end_date}
        }).to_list()

        # Group activities by day
        daily_activity = {}
        for enrollment in enrollments:
            if enrollment.last_activity:
                day = enrollment.last_activity.strftime("%Y-%m-%d")
                daily_activity[day] = daily_activity.get(day, 0) + 1

        activity = [
            ActivityDay(day=day, hours=hours * 0.5)  # Assuming average of 30 minutes per activity
            for day, hours in daily_activity.items()
        ]

        return UserActivityResponse(activity=activity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))