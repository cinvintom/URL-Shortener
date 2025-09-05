from fastapi import APIRouter
from app.api.api_v1.endpoints import urls
from app.api.api_v1.endpoints import redirect

url_shortener_router = APIRouter()
redirect_router = APIRouter()

url_shortener_router.include_router(urls.router, 
                          prefix="",
                          tags=["url-shortener"])

redirect_router.include_router(redirect.router, 
                          prefix="",
                          tags=["redirect"])