from fastapi.testclient import TestClient
from src.endpoints.ims_api import app, fill_db
from src.models.models import Base
from src.endpoints.dependencies import get_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./testsqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def test_setup():
    session = TestingSessionLocal()
    try:
        fill_db(session)
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
test_setup()
base_url = "/ims/rest/"


def test_read_root():
    response = client.get("/")
    assert response.status_code == 404


def test_read_base_url():
    response = client.get(base_url)
    assert response.status_code == 404
