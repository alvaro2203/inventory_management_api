from fastapi import APIRouter, Depends, Query, HTTPException, Query
from typing import List, Optional
from inventory_management.schemas.product import ProductRead, ProductReadDetailed
from inventory_management.schemas.stock_movement import StockMovementRead
from sqlalchemy.orm import Session
from inventory_management.db.database import get_db
from inventory_management.repository.products.crud import get_db_products, get_db_product_by_id, get_db_product_movements


router = APIRouter()

@router.get("/products/", response_model=List[ProductRead])
async def get_products(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 20,
    category_id: Optional[int] = Query(None, description="Filter by category id."),
    search_name: Optional[str] = Query(None, description="Search by name"),
):
    products = get_db_products(db, skip, limit, category_id, search_name)

    if products is None:
        raise HTTPException(
            status_code=404, 
            detail="No products found."
        )
    
    return products


@router.get("/products/detailed", response_model=List[ProductReadDetailed])
async def get_products_detailed(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 20,
    category_id: Optional[int] = Query(None, description="Filter by category id."),
    search_name: Optional[str] = Query(None, description="Search by name"),
):
    products = get_db_products(db, skip, limit, category_id, search_name)

    if products is None:
        raise HTTPException(
            status_code=404, 
            detail="No products found."
        )
    
    return products


@router.get("/products/{product_id}", response_model=Optional[ProductRead])
async def get_product(db: Session = Depends(get_db), product_id: int = None):
    product = get_db_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Product with ID {product_id} not found."
        )
    
    return product


@router.get("/products/detailed/{product_id}", response_model=Optional[ProductReadDetailed])
async def get_product_detailed(db: Session = Depends(get_db), product_id: int = None):
    product = get_db_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Product with ID {product_id} not found."
        )
    
    return product


@router.get("/products/{product_id}/movements/", response_model=List[StockMovementRead])
async def get_product_movements(
    db: Session = Depends(get_db), 
    product_id: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100)
):
    product = get_db_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Product with ID {product_id} not found."
        )
    
    product_movements = get_db_product_movements(db, product_id)    
    return product_movements