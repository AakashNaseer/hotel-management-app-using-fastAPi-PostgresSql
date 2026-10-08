from datetime import datetime, timedelta , timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
from database import get_db

SECRET_KEY = "Offcampus"
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 60
ADMIN_SECRET = "offcampus12"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain:str, hashed: str) -> bool:
    return pwd_context.verify(plain,hashed)

def create_access_token(email: str , role:str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)   
    return jwt.encode({"sub": email, "role": role, "exp": expire}, SECRET_KEY,algorithm=ALGORITHM)

def create_user(db:Session, data, role: str) -> models.User:
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        full_name=data.full_name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
       