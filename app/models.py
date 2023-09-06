from sqlalchemy import Boolean, Column, Integer, String, DATE
# from sqlalchemy.orm import Relationship
from datetime import datetime as dt

from app.database import Base

class Event(Base):
    __tablename__ = "Events"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    description = Column(String, index=True)
    event_date = Column(DATE, default=dt.now().date, index=True)
    checked = Column(Boolean, default=False, index=True)
    work = Column(Boolean, nullable=True, default=None, index=True)
