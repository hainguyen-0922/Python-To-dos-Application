from sqlalchemy import Column, String, Interval
from database import Base
from schemas.base_entity import BaseEntity

class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    rating = Column(Interval, nullable=False)