from datetime import datetime
import enum
from pydantic import BaseModel, Field
from uuid import UUID

class Status(enum.Enum):
    ENABLE = "Enable"
    DISABLE = "Disable"
    
class TaskModel(BaseModel):
    summary: str = Field(min_length=3)
    description: str = Field(min_length=3)
    status: Status = Field(default=Status.DISABLE)
    priority: str = Field(min_length=3)
    user_id: UUID

class TaskViewModel(TaskModel):
    id: UUID    
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_map: True