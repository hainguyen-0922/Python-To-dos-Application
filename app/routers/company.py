from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db_context
from models.company import CompanyModel, CompanyViewModel
from schemas.company import Company
from services import auth as auth_service

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("", response_model=list[CompanyViewModel])
async def get_companies(db: Session = Depends(get_db_context)):
    return db.query(Company).all()