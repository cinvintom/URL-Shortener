from typing import Optional
from pydantic import BaseModel
from app.models.url import UrlType



class URLCreate(BaseModel):
    original_url: str
    short_url: Optional[str] = None
    url_type: Optional[UrlType] = UrlType.RANDOM


class URLResponse(BaseModel):
    short_url: str
    original_url: str

class CustomURLAvailabilityResponse(BaseModel):
    short_url: str
    is_short_url_available: bool
