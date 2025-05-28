from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Ecommerce_Admin_API.db.base_class import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    products: Mapped[List["Product"]] = relationship(back_populates="category")

    __table_args__ = (
        Index('idx_category_name', 'name'),
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    price: Mapped[float] = mapped_column(Float, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category: Mapped["Category"] = relationship(back_populates="products")
    inventory: Mapped["Inventory"] = relationship(back_populates="product", uselist=False)
    sales_details: Mapped[List["SalesDetail"]] = relationship(back_populates="product")

    __table_args__ = (
        Index('idx_product_name', 'name'),
        Index('idx_product_sku', 'sku'),
        Index('idx_product_price', 'price'),
        Index('idx_product_category', 'category_id'),
    ) 