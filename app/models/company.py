from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

class CompanyModel(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3)
    mode: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)

class CompanyViewModel(CompanyModel):
    id: UUID    
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_map: True