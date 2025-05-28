from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from Ecommerce_Admin_API.db.dependencies import get_db_session
from Ecommerce_Admin_API.db.models.product import Category, Product
from Ecommerce_Admin_API.db.models.sales import Inventory, Sales, SalesDetail
from Ecommerce_Admin_API.db.models.schemas import (
    DateRangeFilter,
    SalesAnalyticsResponse,
    SalesCreate,
    SalesResponse,
)

router = APIRouter()


@router.post("/", response_model=SalesResponse)
async def create_sale(
    sale_data: SalesCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """Create a new sale with multiple products."""
    # Start a transaction
    async with session.begin():
        # Create the sale
        sale = Sales(total_amount=0)  # Will be updated after details
        session.add(sale)
        await session.flush()

        total_amount = 0
        for detail in sale_data.details:
            # Check inventory
            inventory = await session.get(Inventory, detail.product_id)
            if not inventory or inventory.quantity < detail.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product ID {detail.product_id}",
                )

            # Create sale detail
            sale_detail = SalesDetail(
                sale_id=sale.id,
                product_id=detail.product_id,
                quantity=detail.quantity,
                unit_price=detail.unit_price,
                total_price=detail.quantity * detail.unit_price,
            )
            session.add(sale_detail)

            # Update inventory
            inventory.quantity -= detail.quantity
            total_amount += sale_detail.total_price

        # Update sale total
        sale.total_amount = total_amount

        # Load all relationships before returning
        query = (
            select(Sales)
            .options(
                joinedload(Sales.details)
                .joinedload(SalesDetail.product)
                .joinedload(Product.category),
            )
            .where(Sales.id == sale.id)
        )
        result = await session.execute(query)
        return result.unique().scalar_one()


@router.get("/", response_model=List[SalesResponse])
async def get_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: AsyncSession = Depends(get_db_session),
):
    """Get sales with optional date filtering."""
    query = select(Sales).options(
        joinedload(Sales.details)
        .joinedload(SalesDetail.product)
        .joinedload(Product.category),
    )
    if start_date:
        query = query.where(Sales.sale_date >= start_date)
    if end_date:
        query = query.where(Sales.sale_date <= end_date)

    result = await session.execute(query)
    return result.unique().scalars().all()


@router.get("/analytics", response_model=SalesAnalyticsResponse)
async def get_sales_analytics(
    period: str = Query(..., regex="^(daily|weekly|monthly|annual)$"),
    date_filter: DateRangeFilter = Depends(),
    session: AsyncSession = Depends(get_db_session),
):
    """Get sales analytics for a specific period."""
    # Base query for sales in date range
    base_query = select(Sales).where(
        and_(
            Sales.sale_date >= date_filter.start_date,
            Sales.sale_date <= date_filter.end_date,
        ),
    )

    # Get total sales and orders
    total_sales_query = select(
        func.sum(Sales.total_amount).label("total_sales"),
        func.count(Sales.id).label("total_orders"),
    ).select_from(base_query.subquery())

    total_result = await session.execute(total_sales_query)
    total_data = total_result.first()

    # Get sales by category
    category_sales_query = (
        select(
            Category.name,
            func.sum(SalesDetail.total_price).label("total"),
        )
        .join(Product, Category.id == Product.category_id)
        .join(SalesDetail, Product.id == SalesDetail.product_id)
        .join(Sales, SalesDetail.sale_id == Sales.id)
        .where(
            and_(
                Sales.sale_date >= date_filter.start_date,
                Sales.sale_date <= date_filter.end_date,
            ),
        )
        .group_by(Category.name)
    )

    category_result = await session.execute(category_sales_query)
    sales_by_category = {row[0]: row[1] for row in category_result}

    # Get sales by product
    product_sales_query = (
        select(
            Product.name,
            func.sum(SalesDetail.total_price).label("total"),
        )
        .join(SalesDetail, Product.id == SalesDetail.product_id)
        .join(Sales, SalesDetail.sale_id == Sales.id)
        .where(
            and_(
                Sales.sale_date >= date_filter.start_date,
                Sales.sale_date <= date_filter.end_date,
            ),
        )
        .group_by(Product.name)
    )

    product_result = await session.execute(product_sales_query)
    sales_by_product = {row[0]: row[1] for row in product_result}

    return SalesAnalyticsResponse(
        total_sales=total_data.total_sales or 0,
        total_orders=total_data.total_orders or 0,
        average_order_value=(
            (total_data.total_sales or 0) / (total_data.total_orders or 1)
        ),
        period=period,
        start_date=date_filter.start_date,
        end_date=date_filter.end_date,
        sales_by_category=sales_by_category,
        sales_by_product=sales_by_product,
    )
