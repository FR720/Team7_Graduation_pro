from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from beanie.odm.fields import PydanticObjectId
from app.auth.auth import get_current_active_user
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.course import CourseList, CourseListItem, CourseDetail, InstructorSchema, CourseCreate, SectionSchema, ModuleSchema
from app.schemas.enrollment import EnrollmentResponse, ModuleProgressUpdate, ModuleProgressResponse

router = APIRouter()

@router.get("", response_model=CourseList)
async def get_courses(
    category: Optional[str] = None,
    level: Optional[str] = None,
    search: Optional[str] = None,
    enrolled: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user)
):
    try:
        query = {}
        if category:
            query["category"] = category
        if level:
            query["level"] = level
        if search:
            query["title"] = {"$regex": search, "$options": "i"}

        courses = await Course.find(query).to_list()
        
        if enrolled is not None:
            user_enrollments = await Enrollment.find({"user_id": str(current_user.id)}).to_list()
            enrolled_course_ids = {str(e.course_id) for e in user_enrollments}

        response_courses = []
        for course in courses:
            is_enrolled = str(course.id) in enrolled_course_ids if enrolled is not None else False
            if enrolled is None or is_enrolled == enrolled:
                progress = 0.0
                if is_enrolled:
                    enrollment = next(e for e in user_enrollments if str(e.course_id) == str(course.id))
                    progress = enrollment.progress

                response_courses.append(CourseListItem(
                    id=str(course.id),
                    title=course.title,
                    description=course.description,
                    duration=course.duration,
                    category=course.category,
                    level=course.level,
                    enrolled=is_enrolled,
                    rating=course.rating,
                    image=course.image,
                    progress=progress
                ))

        return CourseList(courses=response_courses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{course_id}", response_model=CourseDetail)
async def get_course_details(course_id: PydanticObjectId, current_user: User = Depends(get_current_active_user)):
    try:    
        course = await Course.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        instructor = await User.get(course.instructor_id)
        if not instructor:
            raise HTTPException(status_code=404, detail="Instructor not found")
        
        enrollment = await Enrollment.find_one({
            "user_id": str(current_user.id),
            "course_id": str(course_id)
        })
        print("user_id, course_id",current_user, course_id)
        print("enrollment",enrollment)
        # Convert sections to SectionSchema
        sections = [
            SectionSchema(
                id=section.id,
                title=section.title,
                completed=section.completed,
                duration=section.duration,
                modules=[
                    ModuleSchema(
                        id=module.id,
                        type=module.type,
                        title=module.title,
                        duration=module.duration,
                        completed=module.completed,
                        score=module.score,
                        questions=module.questions,
                        pages=module.pages
                    ) for module in section.modules
                ]
            ) for section in course.sections
        ]

        return CourseDetail(
            id=str(course.id),
            title=course.title,
            description=course.description,
            instructor=InstructorSchema(id=str(instructor.id), name=instructor.name),
            category=course.category,
            level=course.level,
            duration=course.duration,
            rating=course.rating,
            image=course.image,
            enrollmentDate=enrollment.enrollment_date if enrollment else None,
            progress=enrollment.progress if enrollment else 0.0,
            sections=sections
        )
    except:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", response_model=CourseDetail)
async def create_course(course_data: CourseCreate, current_user: User = Depends(get_current_active_user)):
    """
    Create a new course with the following structure:
    {
        "title": "Course Title",
        "description": "Course Description",
        "duration": "10h",
        "category": "Programming",
        "level": "beginner",
        "image": "course-image.jpg",
        "sections": [
            {
                "id": "section1",
                "title": "Section 1",
                "duration": "1h",
                "completed": false,
                "modules": [
                    {
                        "id": "module1",
                        "title": "Module 1",
                        "type": "video",
                        "duration": "30m",
                        "completed": false,
                        "questions": 0,
                        "pages": 0
                    }
                ]
            }
        ]
    }
    """
    try:
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can create courses"
            )

        course = Course(
            **course_data.model_dump(),
            instructor_id=str(current_user.id),
            rating=0.0
        )
        await course.insert()

        return CourseDetail(
            id=str(course.id),
            instructor=InstructorSchema(id=str(current_user.id), name=current_user.name),
            **course_data.model_dump(),
            rating=course.rating,
            enrollmentDate=None,
            progress=0.0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/{course_id}/enroll", response_model=EnrollmentResponse)
async def enroll_course(course_id: PydanticObjectId, current_user: User = Depends(get_current_active_user)):
    try:
        course = await Course.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        existing_enrollment = await Enrollment.find_one({
            "user_id": str(current_user.id),
            "course_id": str(course_id)
        })
        if existing_enrollment:
            raise HTTPException(status_code=400, detail="Already enrolled in this course")

        enrollment = Enrollment(
            user_id=str(current_user.id),
            course_id=str(course_id)
        )
        await enrollment.insert()

        return EnrollmentResponse(
            success=True,
            enrollment_id=str(enrollment.id),
            enrollment_date=enrollment.enrollment_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{course_id}/modules/{module_id}/progress", response_model=ModuleProgressResponse)
async def update_module_progress(
    course_id: str,
    module_id: str,
    progress: ModuleProgressUpdate,
    current_user: User = Depends(get_current_active_user)
):
    try:
        enrollment = await Enrollment.find_one({
            "user_id": str(current_user.id),
            "course_id": str(course_id)
        })
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        course = await Course.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Validate module exists in course
        module_found = False
        for section in course.sections:
            for module in section.modules:
                if module.id == module_id:
                    module_found = True
                    break
            if module_found:
                break

        if not module_found:
            raise HTTPException(status_code=404, detail="Module not found in course")

        # Initialize module progress if not exists
        if not hasattr(enrollment, 'module_progress'):
            enrollment.module_progress = {}
        if not hasattr(enrollment, 'module_scores'):
            enrollment.module_scores = {}

        # Update module progress
        enrollment.module_progress[module_id] = progress.completed
        if progress.score is not None:
            enrollment.module_scores[module_id] = min(100, max(0, progress.score))

        # Calculate overall course progress
        total_modules = sum(len(section.modules) for section in course.sections)
        valid_module_progress = {k: v for k, v in enrollment.module_progress.items() 
                            if any(any(m.id == k for m in s.modules) 
                                for s in course.sections)}
        
        completed_modules = sum(1 for completed in valid_module_progress.values() if completed)
        course_progress = min(100, (completed_modules / total_modules) * 100 if total_modules > 0 else 0)

        enrollment.progress = course_progress
        enrollment.last_activity = datetime.utcnow()
        await enrollment.save()

        return ModuleProgressResponse(
            success=True,
            course_progress=course_progress
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))