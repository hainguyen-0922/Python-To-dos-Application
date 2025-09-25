from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ultils.hashpassword import get_password_hash
from database import get_db_context
from models.user import UserAddModel, UserViewModel
from schemas.user import User
from services import auth as auth_service

router = APIRouter(prefix="/user", tags=["User"])

@router.get("", response_model=list[UserViewModel])
async def get_users(user: User = Depends(auth_service.token_interceptor), db: Session = Depends(get_db_context)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    users = (
        db.query(
            User.id,
            User.email,
            User.username,
            User.first_name,
            User.last_name,
            User.is_active,
            User.is_admin,
            User.company_id
        )
        .all()
    )
    return users

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_user(req: UserAddModel, db: Session = Depends(get_db_context)):
    hashed_password = get_password_hash(req.password)

    new_user = User(email=req.email,
        username=req.username,
        first_name=req.first_name,
        last_name=req.last_name,
        hashed_password=hashed_password,
        company_id=req.company_id,
        is_active = req.is_active,
        is_admin = req.is_admin,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user