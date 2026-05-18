from pydantic import BaseModel, field_validator
from typing import Optional

class Product(BaseModel):
    name: str
    category: str
    subcategory: str
    age_group: str
    gender: str
    fabric: str
    color: str
    style:str
    fit:str
    usage:str
    description:str
    tags:str
    brand: Optional[str] = None
    price: float
    

    @field_validator("category")
    def not_empty(cls,value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value
    

    """
    @field_validator("price")
    def price_positive(cls,value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value
    """

class ProductUpdate(BaseModel):

    name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    age_group: Optional[str] = None
    gender: Optional[str] = None
    fabric: Optional[str] = None
    color: Optional[str] = None
    style: Optional[str] = None
    fit: Optional[str] = None
    usage: Optional[str] = None

    description: Optional[str] = None
    tags: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
