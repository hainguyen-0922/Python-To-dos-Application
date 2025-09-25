from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db_context
from fastapi.security import OAuth2PasswordRequestForm
from services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db_context)):
    
    user = auth_service.authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "access_token": auth_service.create_access_token(user),
        "token_type": "bearer"
    }