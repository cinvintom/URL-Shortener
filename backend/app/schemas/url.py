from typing import Optional
from pydantic import BaseModel
from app.models.url import UrlType


class URLCreate(BaseModel):
    original_url: str
    url_type: Optional[UrlType] = UrlType.RANDOM
