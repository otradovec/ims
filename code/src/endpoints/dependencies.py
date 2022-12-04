from src.database.database import SessionLocal

base_url = "/ims/rest/"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
