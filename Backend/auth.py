from datetime import datetime, timedelta, timezone
from typing import Optional, Protocol

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
import hashlib
import hmac
import os
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal
from .config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

PASSWORD_HASH_ALGORITHM = "sha256"
PASSWORD_HASH_ITERATIONS = 100_000
PASSWORD_HASH_SALT_SIZE = 16

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        salt, digest = hashed.split("$", 1)
    except ValueError:
        return False
    test_digest = hashlib.pbkdf2_hmac(
        PASSWORD_HASH_ALGORITHM,
        plain.encode(),
        salt.encode(),
        PASSWORD_HASH_ITERATIONS,
    )
    return hmac.compare_digest(digest, test_digest.hex())

def hash_password(password: str) -> str:
    salt = os.urandom(PASSWORD_HASH_SALT_SIZE).hex()
    digest = hashlib.pbkdf2_hmac(
        PASSWORD_HASH_ALGORITHM,
        password.encode(),
        salt.encode(),
        PASSWORD_HASH_ITERATIONS,
    )
    return f"{salt}${digest.hex()}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = models.User(
        username=username,
        hashed_password=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
