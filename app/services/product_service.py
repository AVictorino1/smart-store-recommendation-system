
from app.database.product_repository import get_connection
from app.database.product_repository import get_all_products
from app.database.product_repository import get_one_product
from app.database.product_repository import delete_product_r
from app.database.product_repository import new_product_r
from app.database.product_repository import update_product_r
from app.database.product_repository import update_product_partial

from app.core.exceptions import NotFoundError

def get_products():
    return get_all_products()


def get_product_id(product_id):
    prod = get_one_product(product_id)
    if prod == None:
        raise NotFoundError("Product not found")
    
    return prod

def new_product(product):
    return new_product_r(product)
    

def delete_product(product_id):
    prod = delete_product_r(product_id) 
    if prod == None: 
        raise NotFoundError("Product not found")

    if prod:
        return {"message" : "Product deleted"}    

def update_product(product_id, updated_product):
    prod = update_product_r(product_id, updated_product)
    if prod == None:
        raise NotFoundError("Product not found")

    return prod


def update_product_partial_s(product_id, updated_product):
    prod = update_product_partial(product_id, updated_product)
    if prod == None:
        raise NotFoundError("Product not found")

    return prod



