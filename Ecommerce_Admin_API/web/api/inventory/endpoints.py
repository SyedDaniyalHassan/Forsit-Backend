from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from Ecommerce_Admin_API.db.dependencies import get_db_session
from Ecommerce_Admin_API.db.models.sales import Inventory
from Ecommerce_Admin_API.db.models.product import Product
from Ecommerce_Admin_API.db.models.schemas import InventoryResponse

router = APIRouter()


@router.get("/", response_model=List[InventoryResponse])
async def get_inventory(
    low_stock: bool = False,
    session: AsyncSession = Depends(get_db_session),
):
    """Get inventory status with optional low stock filter."""
    query = (
        select(Inventory)
        .options(
            joinedload(Inventory.product).joinedload(Product.category)
        )
    )
    if low_stock:
        query = query.where(Inventory.quantity <= Inventory.low_stock_threshold)
    
    result = await session.execute(query)
    return result.unique().scalars().all()


@router.put("/{product_id}", response_model=InventoryResponse)
async def update_inventory(
    product_id: int,
    quantity: int,
    session: AsyncSession = Depends(get_db_session),
):
    """Update inventory quantity for a product."""
    query = (
        select(Inventory)
        .options(
            joinedload(Inventory.product).joinedload(Product.category)
        )
        .where(Inventory.product_id == product_id)
    )
    result = await session.execute(query)
    inventory = result.unique().scalar_one_or_none()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    inventory.quantity = quantity
    inventory.last_updated = datetime.utcnow()
    await session.commit()
    return inventory 