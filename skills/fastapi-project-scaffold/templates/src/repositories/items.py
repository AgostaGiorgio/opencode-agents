import logging
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.clients.postgres_client import PostgresClient
from src.db.models.item import Item, ItemCreate
from src.repositories import queries as q

logger = logging.getLogger(__name__)


class ItemRepository:

    def __init__(self, postgres_client: PostgresClient):
        self.__postgres_client = postgres_client

    async def get_items(self) -> list[Item]:
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_ITEMS)
                rows = result.mappings().all()
                logger.debug(f"Fetched {len(rows)} items from the database.")
                return [Item(**row) for row in rows]
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error fetching items: {e}", exc_info=True)
                return []

    async def get_item(self, item_id: UUID) -> Item | None:
        async with self.__postgres_client.async_session() as session:
            try:
                result = await session.execute(q.GET_ITEM, {"id": str(item_id)})
                row = result.mappings().first()
                return Item(**row) if row else None
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error fetching item '{item_id}': {e}", exc_info=True)
                return None

    async def create_item(self, data: ItemCreate) -> Item | None:
        async with self.__postgres_client.async_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(q.NEW_ITEM, data.to_dict())
                    row = result.mappings().one()
                    logger.debug(f"Item '{data.name}' successfully created.")
                    return Item(**row)
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error creating item '{data.name}': {e}", exc_info=True)
                return None

    async def update_item(self, item_id: UUID, data: ItemCreate) -> Item | None:
        async with self.__postgres_client.async_session() as session:
            try:
                async with session.begin():
                    params = {**data.to_dict(), "id": str(item_id)}
                    result = await session.execute(q.UPDATE_ITEM, params)
                    row = result.mappings().first()
                    if row is None:
                        logger.warning(f"Item '{item_id}' not found.")
                        return None
                    logger.debug(f"Item '{item_id}' successfully updated.")
                    return Item(**row)
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error updating item '{item_id}': {e}", exc_info=True)
                return None

    async def delete_item(self, item_id: UUID) -> bool:
        async with self.__postgres_client.async_session() as session:
            try:
                async with session.begin():
                    result = await session.execute(q.DELETE_ITEM, {"id": str(item_id)})
                    if result.rowcount == 0:
                        logger.warning(f"Item '{item_id}' not found.")
                        return False
                    logger.debug(f"Item '{item_id}' successfully deleted.")
                    return True
            except (SQLAlchemyError, ValidationError) as e:
                logger.error(f"Error deleting item '{item_id}': {e}", exc_info=True)
                return False
