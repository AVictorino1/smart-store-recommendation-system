from app.database.product_repository import get_all_products
from app.database.product_repository import get_one_product
from app.database.product_repository import get_products_id
from app.recommender.rule_based import best_recommendations

def recommendations(product_id):
    
    products = get_all_products()
    prod = get_one_product(product_id)
    recommendations = best_recommendations(prod, products)

    
    return {
        "product" : prod,
        "recommendations": get_products_id(recommendations)}