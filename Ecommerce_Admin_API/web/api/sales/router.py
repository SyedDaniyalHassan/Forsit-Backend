from fastapi import APIRouter

from Ecommerce_Admin_API.web.api.sales.endpoints import router as sales_router

router = APIRouter()
router.include_router(sales_router, prefix="/sales", tags=["sales"]) 