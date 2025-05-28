from fastapi import APIRouter

from Ecommerce_Admin_API.web.api.inventory.router import router as inventory_router
from Ecommerce_Admin_API.web.api.sales.router import router as sales_router

api_router = APIRouter()
api_router.include_router(sales_router)
api_router.include_router(inventory_router)
