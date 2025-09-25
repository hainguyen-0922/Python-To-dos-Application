from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from settings import JWT_ALGORITHM, JWT_SECRET
from schemas.user import User
from ultils.hashpassword import verify_password
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return False

def create_access_token(user: User, expires: Optional[timedelta]=None):
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
        "company_id": str(user.company_id)
    }
    expires_in = datetime.utcnow() + expires if expires else datetime.utcnow() + timedelta(minutes=5)
    claims.update({"exp":expires_in})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)

def token_interceptor(token: str = Depends(oa2_bearer)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User()
        user.username = payload.get("sub")
        user.id = payload.get("id")
        user.first_name = payload.get("first_name")
        user.last_name = payload.get("last_name")
        user.is_admin = payload.get("is_admin")
        user.company_id = payload.get("company_id")
        
        if(user.username is None or user.id is None):
            raise HTTPException(status_code=401, detail="Invalid credential")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credential")
