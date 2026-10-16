"""Service template.

A service holds business logic only. It receives repositories via constructor and
never touches SQL, sessions, or PostgresClient.
"""

import logging

from src.repositories.<entity> import <Entity>Repository

# Adjust the model import path to the project (src.db.models.* or src.models.*).
from src.db.models.<entity> import <Entity>

logger = logging.getLogger(__name__)


class <Entity>Service:

    def __init__(self, <entity>_repository: <Entity>Repository):
        self.__<entity>_repository = <entity>_repository

    async def get_<entities>(self) -> list[<Entity>]:
        logger.debug("Fetching <entities>...")
        return await self.__<entity>_repository.get_<entities>()

    async def add_<entity>(self, data: <Entity>) -> <Entity> | None:
        logger.debug(f"Adding <entity> {data}...")
        return await self.__<entity>_repository.create_<entity>(data)
