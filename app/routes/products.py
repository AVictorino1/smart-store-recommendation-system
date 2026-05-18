from fastapi import APIRouter
from app.models import Product, ProductUpdate
import app.services.product_service 

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/products")
async def get_products():
    return app.services.product_service.get_products()


@router.get("/products/{product_id}")
async def get_products_id(product_id: int):
    return app.services.product_service.get_product_id(product_id)


@router.post("/products")
async def new_product(product: Product):
    return app.services.product_service.new_product(product)


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):

    return app.services.product_service.delete_product(product_id)   


@router.put("/products/{product_id}")
async def update_product(product_id: int, updated_product: ProductUpdate):
    return app.services.product_service.update_product(product_id, updated_product)


@router.patch("/products/{product_id}")
async def update_product(product_id: int, updated_product: ProductUpdate):
    return app.services.product_service.update_product_partial_s(product_id, updated_product)
