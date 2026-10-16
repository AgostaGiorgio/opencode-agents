from dependency_injector import containers, providers

from src.clients.postgres_client import PostgresClient
from src.config.app_config import app_config
from src.repositories.items import ItemRepository
from src.services.items import ItemService


class Container(containers.DeclarativeContainer):

    postgres_client = providers.Singleton(
        PostgresClient, db_url=app_config.postgresql_connection_uri
    )

    item_repository = providers.Factory(ItemRepository, postgres_client=postgres_client)
    item_service = providers.Factory(ItemService, item_repository=item_repository)
