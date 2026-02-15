from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4

from backend.models.db import get_db, User

# create the router with tags for better doc grouping
router = APIRouter(tags=["auth"])

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# directory for uploaded profile images (absolute path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "users")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------
# Response Schemas
# -------------------------------
class MessageResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str

# -------------------------------
# Register Route
# -------------------------------
@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=201,
    summary="Register a new user",
)
async def register_user(
    username: str = Form(...),
    name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """
    Create a new user with optional profile image upload.
    """
    # check for existing user/email
    existing_user = (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered",
        )

    # hash the password
    hashed_password = pwd_context.hash(password)

    # handle profile image if provided
    image_path = None
    if file:
        ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid4()}{ext}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # create and persist user
    new_user = User(
        username=username,
        name=name,
        email=email,
        password=hashed_password,
        profile_image=image_path,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

# -------------------------------
# Login Route
# -------------------------------
@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Authenticate user and return access token",
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Verify credentials and return a JWT access token (stubbed).
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # TODO: implement real JWT creation
    token = "fake-jwt-token"

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        username=user.username,
    )
