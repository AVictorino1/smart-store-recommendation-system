from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes.products import router as products_router
from app.routes.recommendations import router as recommendation_router
from app.core.exceptions import NotFoundError
app = FastAPI()

app.include_router(products_router)
app.include_router(recommendation_router)

@app.exception_handler(NotFoundError)
def not_found_handler(request, exc):
    return JSONResponse(status_code=404,content={"error": str(exc)})







