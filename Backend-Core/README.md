# Course Platform API

A FastAPI-based backend service for an educational platform with chat functionality.

## Features
- User Authentication (JWT)
- Course Management
- User Enrollment
- Chat System with AI Integration
- User Activity Tracking

## Prerequisites
- Python 3.8+
- MongoDB
- pip (Python package manager)

## Installation

1. Create a virtual environment and activate it
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration. Replace with your MongoDB connection string
DATABASE_URL=mongodb://admin:adminpassword@localhost:27017/course_platform?authSource=admin

# JWT Configuration
JWT_SECRET=your_secure_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
API_V1_PREFIX=/api/v1
BACKEND_CORS_ORIGINS=["*"]
```

Make sure to:
- Replace `your_secure_secret_key` with a strong secret key
- Update the MongoDB connection string according to your setup
- Adjust CORS origins as needed for production

## Running the Application

1. Start MongoDB service
2. Run the FastAPI application:
```bash
python3 -m uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

- Postman: You can import the Postman collection from `CoursePlatformAPI.postman_collection.json` to test the API endpoints.

## Implementing AI Chat Integration

To implement the AI chat functionality, locate the chat route in `app/routes/chat.py`. Replace the mock response generation with your AI implementation:

```python
# Current mock implementation:
ai_message_content = f"This is a mock response for the course {course.title}. You asked: {message.message}"

# Replace with your AI chat implementation:
ai_message_content = await generate_ai_response(course.title, message.message)
```

Implement the `generate_ai_response` function to integrate with your preferred AI service.