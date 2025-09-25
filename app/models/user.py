from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class UserModel(BaseModel):
    email: str = Optional[str]
    username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)    
    company_id: Optional[UUID]
    is_active: bool
    is_admin: bool    

class UserAddModel(UserModel):
    password: str = Field(min_length=3)

class UserViewModel(UserModel):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_map: True