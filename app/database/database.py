import asyncio
import os
import datetime

from typing import List, Tuple
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from database.models import Base, Task 

from config.config import Config

engine = None
async_session = None

async def init_db() -> None:
    global engine, async_session
    
    if os.path.exists("todo.db"):
        await asyncio.to_thread(os.remove, "todo.db")
    
    engine = create_async_engine(Config.DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
async def add_task(user_id: int, task_text: str, deadline: datetime) -> bool:
    async with async_session() as session:
        try:
            task = Task(
                user_id=user_id,
                task=task_text,
                deadline=deadline,
                position=None 
            )
            session.add(task)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            raise e
        

async def get_all_tasks(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            Task.__table__.select().where(Task.user_id == user_id).order_by(Task.created_at)
        )
        
        return result.all()
    
async def delete_by_position(user_id: int, position: int) -> bool:
    async with async_session() as session:
        tasks = await session.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.deadline.asc())
        )
        
        tasks_list = tasks.scalars().all()
        
        if 1 <= position <= len(tasks_list):
            task_to_delete = tasks_list[position-1]
            await session.delete(task_to_delete)
            await session.commit()
            return True
        
        return False
        
async def get_tasks_with_numbers(user_id: int) -> List[Tuple[int, Task]]:
    async with async_session() as session:
        result = await session.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.deadline.asc())
        )
        tasks = result.scalars().all()
        
        return list(enumerate(tasks, start=1))