from fastapi import FastAPI
from inventory_management.api.v1.products.router import router as product_router

app = FastAPI(title="Inventory Management API")

app.include_router(
    product_router,
    prefix="/api/v1",
    tags=["Products"]
)