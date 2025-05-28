from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    sku: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    category_id: int


class ProductCreate(ProductBase):
    initial_stock: int = Field(..., ge=0)
    low_stock_threshold: int = Field(10, ge=0)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryResponse

    class Config:
        from_attributes = True


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    low_stock_threshold: int
    last_updated: datetime
    product: ProductResponse

    class Config:
        from_attributes = True


class SalesDetailBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class SalesCreate(BaseModel):
    details: List[SalesDetailBase]


class SalesDetailResponse(SalesDetailBase):
    id: int
    sale_id: int
    total_price: float
    created_at: datetime
    product: ProductResponse

    class Config:
        from_attributes = True


class SalesResponse(BaseModel):
    id: int
    sale_date: datetime
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
    details: List[SalesDetailResponse]

    class Config:
        from_attributes = True


class DateRangeFilter(BaseModel):
    start_date: datetime
    end_date: datetime


class SalesAnalyticsResponse(BaseModel):
    total_sales: float
    total_orders: int
    average_order_value: float
    period: str  # daily, weekly, monthly, annual
    start_date: datetime
    end_date: datetime
    sales_by_category: dict[str, float]
    sales_by_product: dict[str, float] 