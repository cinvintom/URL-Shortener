from fastapi import APIRouter, Depends, status, HTTPException, FastAPI, Request
from typing import Dict
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


from app.api.deps import get_db
from app.schemas.url import URLCreate, URLResponse, CustomURLAvailabilityResponse
from app.error_code.common_errors import CommonErrorCode
from app.error_code.error_manager import error_manager
from app.services.urls import UrlServices
from app.core.config import settings

# Create FastAPI app instance for rate limiter setup
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

router = APIRouter()

@router.post(
    "/generate",
    response_model=URLResponse,
    responses={
        200: {"description": "URL already exists", "model": URLResponse},
        201: {"description": "New URL created", "model": URLResponse},
    },
)
@limiter.limit("10/minute")
def create_url(
    *,
    db: Session = Depends(get_db),
    url_in: URLCreate,
    request: Request = None
) -> Dict[str, str]:
    """
    Generates a shortened URL for the provided original URL.

    Accepts an original URL and an optional custom short URL or URL type.
    """
    try:
        url = UrlServices.create_url_mapping(db=db, url_in=url_in)
        return url
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        raise error_manager.error_responder(
            status_code=500,
            error_code=CommonErrorCode.INTERNAL_SERVER_ERROR,
            error_message=f"An unexpected error occurred: {exc}"
        )


@router.get(
    "/custom_url/available/{short_url}",
    response_model=CustomURLAvailabilityResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("100/minute")
def check_if_custom_url_exists(
    *,
    db: Session = Depends(get_db),
    short_url: str,
    request: Request

) -> CustomURLAvailabilityResponse:
    """
    Checks if the provided custom short URL is available.

    Returns:
        CustomURLAvailabilityResponse: Contains the short_url and its availability status.
    """
    try:
        url = UrlServices.get_url_mapping_by_short_url(db=db, short_url=short_url)
        return CustomURLAvailabilityResponse(
            short_url=short_url,
            is_short_url_available=url is None
        )
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        raise error_manager.error_responder(
            status_code=500,
            error_code=CommonErrorCode.INTERNAL_SERVER_ERROR,
            error_message=f"An unexpected error occurred: {exc}"
        )