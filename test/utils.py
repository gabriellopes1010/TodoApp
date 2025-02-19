from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pytest

from ..models import Todos
from ..database import Base
from ..main import app

SQLALCHEMY_DATABASE_URL = (
    "postgresql://gabriellopes1010:teste1234@localhost/TodoApplicationDatabaseTest"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "gabriellopes1010", "id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture
def tests_todo():
    todo = Todos(
        description="Need to learn everyday",
        complete=False,
        priority=5,
        title="Learn to code!",
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as con:
        con.execute(text("DELETE FROM todos"))
        con.execute(text("SELECT setval('todos_id_seq', 1, false)"))
        con.commit()
