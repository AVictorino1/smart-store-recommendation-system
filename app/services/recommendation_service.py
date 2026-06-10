from app.database.product_repository import get_all_products
from app.database.product_repository import get_one_product
from app.database.product_repository import get_products_id
from app.recommender.pipeline import recomm

def recommendations(product_id):
    
    prod = get_one_product(product_id)
    recommendations = recomm(product_id)

    
    return {
        "product" : prod,
        "recommendations": recommendations}