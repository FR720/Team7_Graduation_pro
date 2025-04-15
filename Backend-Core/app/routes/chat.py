from fastapi import APIRouter, Depends, HTTPException
from app.auth.auth import get_current_active_user
from app.models.user import User
from app.models.chat import ChatMessage
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatHistoryResponse
from datetime import datetime

router = APIRouter()

@router.post("/{course_id}/chat", response_model=ChatMessageResponse)
async def send_message(
    course_id: str,
    message: ChatMessageRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Verify course exists and user is enrolled
        course = await Course.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        enrollment = await Enrollment.find_one({
            "user_id": str(current_user.id),
            "course_id": str(course_id)
        })
        if not enrollment:
            raise HTTPException(status_code=403, detail="Not enrolled in this course")

        # Save user message
        user_message = ChatMessage(
            course_id=str(course_id),
            user_id=str(current_user.id),
            sender="user",
            message=message.message
        )
        await user_message.insert()

        # Generate mock AI response
        ai_message_content = f"This is a mock response for the course {course.title}. You asked: {message.message}"

        # Save AI response
        ai_message = ChatMessage(
            course_id=str(course_id),
            user_id=str(current_user.id),
            sender="ai",
            message=ai_message_content
        )
        await ai_message.insert()

        return ChatMessageResponse(
            response={
                "sender": "ai",
                "message": ai_message_content,
                "timestamp": ai_message.timestamp
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{course_id}/chat", response_model=ChatHistoryResponse)
async def get_chat_history(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Verify course exists and user is enrolled
        course = await Course.get(str(course_id))
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        enrollment = await Enrollment.find_one({
            "user_id": str(current_user.id),
            "course_id": str(course_id)
        })
        if not enrollment:
            raise HTTPException(status_code=403, detail="Not enrolled in this course")

        # Get chat history
        db_messages = await ChatMessage.find({
            "course_id": str(course_id),
            "user_id": str(current_user.id)
        }).sort("timestamp").to_list()

        # Convert database messages to schema messages
        messages = [
            {"sender": msg.sender, "message": msg.message, "timestamp": msg.timestamp}
            for msg in db_messages
        ]

        return ChatHistoryResponse(messages=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))