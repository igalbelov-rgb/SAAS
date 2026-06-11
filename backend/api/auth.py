from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from app.database import get_session
from app.models import User
from app.crypto import hash_password, verify_password, create_access_token  # 🔥 ייבוא הפונקציות הישירות

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# --- סכמות קלט/פלט (Schemas) ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    is_active: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Endpoints ---

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    # 1. בדיקה האם המשתמש כבר קיים במערכת
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. הצפנת הסיסמה ויצירת המשתמש החדש (שימוש בפונקציה הישירה)
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        full_name=user_data.full_name
    )
    
    # 3. שמירה בדאטאבייס
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user


@router.post("/login")
def login_user(login_data: UserLogin, session: Session = Depends(get_session)):
    # 1. חיפוש המשתמש לפי אימייל
    user = session.exec(select(User).where(User.email == login_data.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
         )

    # 2. אימות הסיסמה המוצפנת
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. יצירת ה-JWT Token המאובטח למשתמש
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    # 4. החזרת המבנה הסטנדרטי שה-Client מצפה לו
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name}
    }