from app.models.url import UrlMapping
from app.schemas.url import URLCreate, UrlType
from sqlalchemy.orm import Session
from app.utils.url_helpers import URLUtils
from app.crud.url import CRUDUrl

crud_url = CRUDUrl()


class UrlServices:
    @staticmethod
    def create_url_mapping(db: Session, url_in: URLCreate) -> UrlMapping:
        """
        Create a new URL mapping in the database.

        Args:
            db (SessionLocal): The database session.
            url_in (URLCreate): The URL creation schema containing the original URL.

        Returns:
            UrlMapping: The created UrlMapping object.
        """
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
            url_type=UrlType.RANDOM,
        )
        crud_url.create_url_mapping(db=db, url_mapping=db_url)
        return db_url

    @staticmethod
    def get_url_mapping(db: Session, short_url: str) -> UrlMapping:
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