"""Repository template.

Replace <Entity> / <entities> / <table> and the imports to match the project.

Rules:
- class, not @classmethod; receive PostgresClient in __init__.
- one session per method via self.__postgres_client.async_session().
- SQL lives in queries.py, referenced as q.NAME.
- catch (SQLAlchemyError, ValidationError) with exc_info=True; never `except Exception`.
- multi-statement writes go inside one `async with session.begin():`.
"""

import logging

from src.clients.postgres_client import PostgresClient
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

# Adjust the model import path to the project (src.db.models.* or src.models.*).
from src.db.models.<entity> import <Entity>

from src.repositories import queries as q

logger = logging.getLogger(__name__)


class <Entity>Repository:

    def __init__(self, postgres_client: PostgresClient):
        self.__postgres_client = postgres_client

    async def get_<entities>(self) -> list[<Entity>]:
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_<ENTITIES>)
                rows = result.mappings().all()
                return [<Entity>(**row) for row in rows]
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error fetching <entities>: {e}", exc_info=True)
                return []

    async def get_<entity>(self, entity_id) -> <Entity> | None:
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_<ENTITY>, {"id": str(entity_id)})
                row = result.mappings().first()
                return <Entity>(**row) if row else None
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error fetching <entity> '{entity_id}': {e}", exc_info=True)
                return None

    async def create_<entity>(self, data: <Entity>) -> <Entity> | None:
        async with self.__postgres_client.async_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(q.NEW_<ENTITY>, data.to_dict())
                    new_id = result.scalar()
                    data.id = new_id
                    return data
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error creating <entity>: {e}", exc_info=True)
                return None

    async def update_<entity>(self, entity_id, data: <Entity>) -> bool:
        async with self.__postgres_client.async_session() as session:
            try:
                async with session.begin():
                    params = {**data.to_dict(), "id": str(entity_id)}
                    result = await session.execute(q.UPDATE_<ENTITY>, params)
                    if result.rowcount == 0:
                        return False
                    return True
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error updating <entity> '{entity_id}': {e}", exc_info=True)
                return False

    async def delete_<entity>(self, entity_id) -> bool:
        async with self.__postgres_client.async_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(q.DELETE_<ENTITY>, {"id": str(entity_id)})
                    if result.rowcount == 0:
                        return False
                    return True
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error deleting <entity> '{entity_id}': {e}", exc_info=True)
                return False

    async def do_multi_step_write(self, entity_id, payload) -> bool:
        """Atomic multi-statement write: everything commits or nothing does."""
        async with self.__postgres_client.async_session() as session:
            try:
                async with session.begin():
                    await session.execute(q.STEP_ONE, {"id": str(entity_id), **payload})
                    await session.execute(q.STEP_TWO, {"id": str(entity_id)})
                    return True
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error in multi-step write '{entity_id}': {e}", exc_info=True)
                return False
