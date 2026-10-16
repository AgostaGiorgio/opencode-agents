import logging
from uuid import UUID

from src.db.models.item import Item, ItemCreate
from src.repositories.items import ItemRepository

logger = logging.getLogger(__name__)


class ItemService:

    def __init__(self, item_repository: ItemRepository):
        self.__item_repository = item_repository

    async def get_items(self) -> list[Item]:
        logger.debug("Fetching items...")
        return await self.__item_repository.get_items()

    async def get_item(self, item_id: UUID) -> Item | None:
        logger.debug(f"Fetching item {item_id}...")
        return await self.__item_repository.get_item(item_id)

    async def add_item(self, data: ItemCreate) -> Item | None:
        logger.debug(f"Adding item '{data.name}'...")
        return await self.__item_repository.create_item(data)

    async def update_item(self, item_id: UUID, data: ItemCreate) -> Item | None:
        logger.debug(f"Updating item {item_id}...")
        return await self.__item_repository.update_item(item_id, data)

    async def delete_item(self, item_id: UUID) -> bool:
        logger.debug(f"Deleting item {item_id}...")
        return await self.__item_repository.delete_item(item_id)
