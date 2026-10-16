"""Dependency-injection graph.

- postgres_client is a Singleton (one engine/session factory per app).
- repositories are Factory, built with the shared client.
- services are Factory, built with their repositories.
- Wire the router modules in main.py: container.wire(modules=[router_module, ...]).
"""

from dependency_injector import containers, providers

from src.clients.postgres_client import PostgresClient
from src.config.app_config import app_config
from src.repositories.<entity> import <Entity>Repository
from src.services.<entity> import <Entity>Service


class Container(containers.DeclarativeContainer):

    postgres_client = providers.Singleton(
        PostgresClient, db_url=app_config.postgresql_connection_uri
    )

    <entity>_repository = providers.Factory(
        <Entity>Repository, postgres_client=postgres_client
    )

    <entity>_service = providers.Factory(
        <Entity>Service, <entity>_repository=<entity>_repository
    )
