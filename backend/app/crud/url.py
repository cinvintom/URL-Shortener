from sqlalchemy.orm import Session
from app.models.url import UrlMapping


class CRUDUrl:
    """
    CRUD operations for UrlMapping model.
    """

    def get_url_by_short_url(self, db: Session, short_url: str) -> UrlMapping:
        """
        Retrieve a UrlMapping object by its short URL.

        Args:
            db (Session): SQLAlchemy database session.
            short_url (str): The short URL string.

        Returns:
            UrlMapping: The UrlMapping object if found, else None.
        """
        return db.query(UrlMapping).filter(UrlMapping.short_url == short_url).first()

    def get_url_by_original_url(self, db: Session, original_url: str) -> UrlMapping:
        """
        Retrieve a UrlMapping object by its original URL.

        Args:
            db (Session): SQLAlchemy database session.
            original_url (str): The original URL string.

        Returns:
            UrlMapping: The UrlMapping object if found, else None.
        """
        return db.query(UrlMapping).filter(UrlMapping.original_url == original_url).first()

    def create_url_mapping(self, db: Session, url_mapping: UrlMapping) -> UrlMapping:
        """
        Create and persist a new UrlMapping object in the database.

        Args:
            db (Session): SQLAlchemy database session.
            url_mapping (UrlMapping): The UrlMapping object to be added.

        Returns:
            UrlMapping: The persisted UrlMapping object.
        """
        db.add(url_mapping)
        db.commit()
        db.refresh(url_mapping)
        return url_mapping
