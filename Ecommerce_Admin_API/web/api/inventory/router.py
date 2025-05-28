from fastapi import APIRouter

from Ecommerce_Admin_API.web.api.inventory.endpoints import router as inventory_router

router = APIRouter()
router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
