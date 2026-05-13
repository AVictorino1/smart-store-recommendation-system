from fastapi import APIRouter
import app.services.recommendation_service


router = APIRouter()

@router.get("/recommendations/{product_id}")
async def recommendations(product_id: int):
    return app.services.recommendation_service.recommendations(product_id)
    