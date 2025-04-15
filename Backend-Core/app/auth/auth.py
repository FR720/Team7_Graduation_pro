from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.core.config import settings
from app.schemas.auth import UserCreate, Token, LoginSchema, UserResponse

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_user(email: str) -> Optional[User]:
    return await User.find_one({"email": email})

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await get_user(email)
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    try:
        if await get_user(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = User(
            email=user_data.email,
            name=user_data.name,
            password=get_password_hash(user_data.password),
            is_admin=user_data.is_admin
        )
        await user.insert()

        access_token = create_access_token(data={"sub": user.email})
        return Token(
            token=access_token,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                created_at=user.created_at,
                is_admin=user.is_admin
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login", response_model=Token)
async def login(login_data: LoginSchema):
    try:
        user = await get_user(login_data.email)
        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token = create_access_token(data={"sub": user.email})
        return Token(
            token=access_token,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                created_at=user.created_at,
                is_admin=user.is_admin
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))