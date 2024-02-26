from sqlalchemy import select

from database import new_session, TaskORM
from shemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_one(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = task.model_dump()

            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls)->list[STask]:
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models=result.scalars().all()
            task_shemas = [STask.model_validate(task_models) for task in task_models]
            return task_shemas