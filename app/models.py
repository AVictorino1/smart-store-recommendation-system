from pydantic import BaseModel, field_validator
from typing import Optional

class Product(BaseModel):
    name: str
    price: int
    category: Optional[str] = None
    brand: Optional[str] = None

    @field_validator("name","category","brand")
    def not_empty(cls,value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value
    
    @field_validator("price")
    def price_positive(cls,value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value
