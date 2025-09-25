from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db_context
from models.task import TaskModel, TaskViewModel
from schemas.task import Task
from schemas.user import User
from services import auth as auth_service

router = APIRouter(prefix="/task", tags=["Task"])

@router.get("", response_model=list[TaskViewModel])
async def get_tasks(user: User = Depends(auth_service.token_interceptor),db: Session = Depends(get_db_context)):
    if user.is_admin:
        return db.query(Task).join(User, Task.user_id == User.id).filter(User.company_id == user.company_id).all()
    return db.query(Task).filter(Task.user_id == User.id).all()

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_task(req: TaskModel, user: User = Depends(auth_service.token_interceptor), db: Session = Depends(get_db_context)):
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    new_task = Task(**req.dict()) 
    new_task.created_at = datetime.utcnow(),
    new_task.updated_at=datetime.utcnow()
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task