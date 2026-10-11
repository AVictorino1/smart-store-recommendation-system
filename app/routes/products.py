from fastapi import APIRouter
from app.models import Product, ProductUpdate, RegeneratedModel
import app.services.product_service 
import app.services.business_service
import app.services.regenerate_service
import json
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

@router.post("/regenerate")
async def regenerate_product(data: RegeneratedModel):
    business = app.services.business_service.get_business()
    
    trigger_fields = json.loads(business["trigger_fields"])
    regenerated_fields = json.loads(business["regenerated_fields"])
    
    response = data.product.model_dump()
    for field in data.fields:
        if field not in trigger_fields:
            return {"message": "Campo no es trigger field"}
        else:
            values = response[field]
            response = app.services.regenerate_service.regenerate_product(
                    response, field, values, regenerated_fields
                )
    
    return response
