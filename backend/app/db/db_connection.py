from app.db.session import SessionLocal
from sqlalchemy.orm import Session


class DBConnection:
    def get_db(self):
        self.db: Session = SessionLocal()

    def close_connection(self):
        self.db.close()
