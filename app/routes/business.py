from fastapi import APIRouter
import app.services.business_service


router = APIRouter()

@router.get("/business/schema")
async def business_schema():
    return app.services.business_service.get_business_schema_s()
    