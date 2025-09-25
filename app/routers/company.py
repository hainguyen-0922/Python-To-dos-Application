from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db_context
from models.company import CompanyViewModel
from schemas.company import Company

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("", response_model=list[CompanyViewModel])
async def get_companies(db: Session = Depends(get_db_context)):
    return db.query(Company).all()