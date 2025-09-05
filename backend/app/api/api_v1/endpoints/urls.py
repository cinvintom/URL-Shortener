from fastapi import APIRouter, Depends, status, HTTPException
from typing import Dict
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.url import URLCreate
from app.error_code.common_errors import CommonErrorCode
from app.error_code.error_manager import error_manager
from app.services.urls import UrlServices

router = APIRouter()


@router.post("/generate", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
def create_url(
    *,
    db: Session = Depends(get_db),
    url_in: URLCreate
) -> Dict[str, str]:
    """
    Generates a shortened URL for the provided original URL.

    Accepts an original URL and an optional custom short URL or URL type.
    """
    try:
        url = UrlServices.create_url_mapping(db=db, url_in=url_in)
        return {
            "msg": "URL generated successfully",
            "short_url": url.short_url,
            "original_url": url.original_url
        }
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        raise error_manager.error_responder(
            status_code=500,
            error_code=CommonErrorCode.INTERNAL_SERVER_ERROR,
            error_message=f"An unexpected error occurred: {exc}"
        )
