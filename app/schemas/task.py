from sqlalchemy import Enum, Uuid, Column, String
from models.task import Status
from database import Base
from schemas.base_entity import BaseEntity

class Task(Base, BaseEntity):
    __tablename__ = "tasks"

    summary = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(Status), nullable=False)
    priority = Column(String, nullable=False)
    user_id = Column(Uuid, nullable=False)