from app.database.business_repository import get_business_info, get_business_schema, update_business_info
from app.core.exceptions import NotFoundError

def get_business():
    business = get_business_info()
    if business is None:
        raise NotFoundError("Business info not found")
    return business

def get_business_schema_s():
    business_schema = get_business_schema()
    if business_schema is None:
        raise NotFoundError("Business schema not found")
    return business_schema

def update_business(field: str, value: str):
    business = get_business_info()
    if business is None:
        raise NotFoundError("Business info not found")
    update_business_info(field, value)
    return get_business_info()