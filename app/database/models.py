from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    task = Column(String(512))
    created_at = Column(DateTime, default=datetime.now)
    deadline = Column(DateTime)
    position = Column(Integer)