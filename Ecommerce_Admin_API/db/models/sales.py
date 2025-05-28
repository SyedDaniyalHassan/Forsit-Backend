from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from Ecommerce_Admin_API.db.base_class import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), unique=True, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=10)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product: Mapped["Product"] = relationship(back_populates="inventory")

    __table_args__ = (
        Index('idx_inventory_product', 'product_id'),
        Index('idx_inventory_quantity', 'quantity'),
    )


class SalesStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Sales(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sale_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    total_amount: Mapped[float] = mapped_column(Float, index=True)
    status: Mapped[SalesStatus] = mapped_column(Enum(SalesStatus), default=SalesStatus.COMPLETED, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    details: Mapped[List["SalesDetail"]] = relationship(back_populates="sale")

    __table_args__ = (
        Index('idx_sales_date', 'sale_date'),
        Index('idx_sales_amount', 'total_amount'),
        Index('idx_sales_status', 'status'),
    )


class SalesDetail(Base):
    __tablename__ = "sales_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sale_id: Mapped[int] = mapped_column(Integer, ForeignKey("sales.id"), index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)
    total_price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    sale: Mapped["Sales"] = relationship(back_populates="details")
    product: Mapped["Product"] = relationship(back_populates="sales_details")

    __table_args__ = (
        Index('idx_sales_detail_sale', 'sale_id'),
        Index('idx_sales_detail_product', 'product_id'),
    ) 