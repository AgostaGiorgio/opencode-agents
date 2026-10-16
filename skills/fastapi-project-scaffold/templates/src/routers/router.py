from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from src.db.models.item import Item, ItemCreate
from src.di import Container
from src.services.items import ItemService

api_router = APIRouter()


@api_router.get("/items", response_model=list[Item], status_code=200)
@inject
async def get_items(
    item_service: ItemService = Depends(Provide[Container.item_service]),
) -> list[Item]:
    return await item_service.get_items()


@api_router.get("/items/{item_id}", response_model=Item, status_code=200)
@inject
async def get_item(
    item_id: UUID,
    item_service: ItemService = Depends(Provide[Container.item_service]),
) -> Item:
    item = await item_service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item


@api_router.post("/items", response_model=Item, status_code=201)
@inject
async def create_item(
    payload: ItemCreate,
    item_service: ItemService = Depends(Provide[Container.item_service]),
) -> Item:
    created = await item_service.add_item(payload)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create item.")
    return created


@api_router.put("/items/{item_id}", response_model=Item, status_code=200)
@inject
async def update_item(
    item_id: UUID,
    payload: ItemCreate,
    item_service: ItemService = Depends(Provide[Container.item_service]),
) -> Item:
    updated = await item_service.update_item(item_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found.")
    return updated


@api_router.delete("/items/{item_id}", status_code=204)
@inject
async def delete_item(
    item_id: UUID,
    item_service: ItemService = Depends(Provide[Container.item_service]),
) -> None:
    deleted = await item_service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found.")
