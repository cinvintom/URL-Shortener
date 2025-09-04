from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.url import CRUDUrl
from app.error_code.common_errors import CommonErrorCode
from app.error_code.error_manager import error_manager

crud_url = CRUDUrl()

router = APIRouter()


@router.get("/{short_code}", response_class=RedirectResponse, status_code=307)
def redirect_to_url(short_code: str, db: Session = Depends(get_db)) -> RedirectResponse:
    """
    Redirect to the original URL based on the short code.
    """
    url_obj = crud_url.get_url_by_short_url(db=db, short_url=short_code)
    if not url_obj:
        raise error_manager.error_responder(
            status_code=404,
            error_code=CommonErrorCode.SHORT_URL_NOT_FOUND,
        )
    return RedirectResponse(url=url_obj.original_url, status_code=307)
