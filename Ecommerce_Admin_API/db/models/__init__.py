"""Database models package."""

from Ecommerce_Admin_API.db.models.product import Category, Product
from Ecommerce_Admin_API.db.models.sales import Inventory, Sales, SalesDetail

__all__ = [
    "Category",
    "Product",
    "Sales",
    "SalesDetail",
    "Inventory",
]


def load_all_models() -> None:
    """Load all models to ensure they are registered with SQLAlchemy."""
    # Import all models here to ensure they are registered
    from Ecommerce_Admin_API.db.models.product import Category, Product
    from Ecommerce_Admin_API.db.models.sales import Inventory, Sales, SalesDetail
