from fastapi import APIRouter, Depends, status, HTTPException, FastAPI, Request
from typing import Dict
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from prometheus_client import Counter, Histogram, generate_latest
import time

from app.api.deps import get_db
from app.schemas.url import URLCreate, URLResponse, CustomURLAvailabilityResponse
from app.error_code.common_errors import CommonErrorCode
from app.error_code.error_manager import error_manager
from app.services.urls import UrlServices
from app.core.config import settings

# Prometheus metrics
REQUEST_COUNT = Counter(
    "url_requests_total", "Total URL requests", ["method", "endpoint"]
)
REQUEST_DURATION = Histogram(
    "url_request_duration_seconds", "Request duration"
)

# Create FastAPI app instance for rate limiter setup
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

router = APIRouter()


@router.get("/metrics")
def metrics():
    """
    Expose Prometheus metrics for monitoring.

    Returns:
        bytes: The latest Prometheus metrics in the default exposition format.
    """
    return generate_latest()

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
    Generate a shortened URL for the provided original URL.

    This endpoint accepts an original URL and an optional custom short URL or URL type.
    If the URL already exists, returns the existing mapping; otherwise, creates a new one.

    Args:
        db (Session): The database session dependency.
        url_in (URLCreate): The URL creation schema containing the original and optional custom short URL.
        request (Request, optional): The FastAPI request object.

    Returns:
        URLResponse: The response containing the short URL and original URL.
    """
    start_time = time.time()
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
    finally:
        endpoint = "/generate"
        method = "POST"
        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        REQUEST_DURATION.observe(time.time() - start_time)


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
    Check if the provided custom short URL is available.

    This endpoint verifies whether a given custom short URL is already in use.

    Args:
        db (Session): The database session dependency.
        short_url (str): The custom short URL to check.
        request (Request): The FastAPI request object.

    Returns:
        CustomURLAvailabilityResponse: Contains the short_url and its availability status.
    """
    start_time = time.time()
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
    finally:
        endpoint = "/custom_url/available/{short_url}"
        method = "GET"
        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
        REQUEST_DURATION.observe(time.time() - start_time)