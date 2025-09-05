from app.models.url import UrlMapping
from app.schemas.url import URLCreate, UrlType
from sqlalchemy.orm import Session
from app.utils.url_helpers import URLUtils
from app.crud.url import CRUDUrl
from app.schemas.url import URLResponse
from app.core.config import settings
from app.error_code.common_errors import CommonErrorCode
from app.error_code.error_manager import error_manager

crud_url = CRUDUrl()


class UrlServices:
    @staticmethod
    def check_if_url_exists(db: Session, url_in: URLCreate) -> bool:
        """
        Check if the URL exists in the database.

        Args:
            db (Session): The database session.
            url_in (URLCreate): The URL creation schema containing the original URL.

        Returns:
            bool: True if the URL exists, False otherwise.
        """
        return crud_url.get_url_by_original_url(db=db, original_url=url_in.original_url) is not None

    @staticmethod
    def check_if_custom_url_exists(db: Session, short_url: str) -> None:
        """
        Check if the custom URL exists in the database.
        """
        if crud_url.get_url_by_short_url(db=db, short_url=short_url) is not None:
             raise error_manager.error_responder(
                            status_code=400,
                            error_code=CommonErrorCode.CUSTOM_URL_ALREADY_EXISTS,
                        )
    @staticmethod
    def create_url_mapping(db: Session, url_in: URLCreate) -> URLResponse:
        """
        Create a new URL mapping in the database.

        Args:
            db (Session): The database session.
            url_in (URLCreate): The URL creation schema containing the original URL.

        Returns:
            UrlMapping: The created UrlMapping object.
        """
        short_url_exists = False
        if UrlServices.check_if_url_exists(db=db, url_in=url_in):
            db_obj = UrlServices.get_url_mapping_by_original_url(
                db=db, original_url=url_in.original_url
            )
            if url_in.short_url and url_in.url_type == UrlType.CUSTOM:
                if db_obj.short_url != url_in.short_url:
                    UrlServices.check_if_custom_url_exists(
                            db=db, short_url=url_in.short_url
                    )
                    db_obj.short_url = url_in.short_url
                    crud_url.update_url_mapping(db=db, url_mapping=db_obj)
            short_url_exists = True
        else:
            if url_in.short_url and url_in.url_type == UrlType.CUSTOM:
                UrlServices.check_if_custom_url_exists(
                    db=db, short_url=url_in.short_url
                )
                short_url = url_in.short_url
            else:
                while True:
                    short_url = URLUtils.generate_random_short_url()
                    existing_url = db.query(UrlMapping).filter(
                        UrlMapping.short_url == short_url
                    ).first()
                    if not existing_url:
                        break

            db_url = UrlMapping(
                original_url=url_in.original_url,
                short_url=short_url,
                url_type=url_in.url_type,
            )
            db_obj = crud_url.create_url_mapping(db=db, url_mapping=db_url)
        return URLResponse(
            short_url=f"http://localhost:{settings.BACKEND_PORT}/{db_obj.short_url}",
            original_url=db_obj.original_url,
            is_short_url_exists=short_url_exists,
            created_at=db_obj.created_at,
        )

    @staticmethod
    def get_url_mapping_by_short_url(db: Session, short_url: str) -> UrlMapping:
        """
        Retrieve a URL mapping from the database by its short URL.

        Args:
            db (SessionLocal): The database session.
            short_url (str): The short URL string.

        Returns:
            UrlMapping: The UrlMapping object if found, else None.
        """
        return crud_url.get_url_by_short_url(db=db, short_url=short_url)

    @staticmethod
    def get_url_mapping_by_original_url(
        db: Session, original_url: str
    ) -> UrlMapping:
        """
        Retrieve a URL mapping from the database by its original URL.

        Args:
            db (SessionLocal): The database session.
            original_url (str): The original URL string.

        Returns:
            UrlMapping: The UrlMapping object if found, else None.
        """
        return crud_url.get_url_by_original_url(db=db, original_url=original_url)