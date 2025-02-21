from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

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
    return {"username": "gabrielsiqueira", "id": 1, "user_role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_user():
    user = Users(
        username="gabrielsiqueira",
        email="gabrielsiqueira@email.com",
        first_name="Gabriel",
        last_name="Siqueira",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as con:
        con.execute(text("DELETE FROM users"))
        con.execute(text("SELECT setval('users_id_seq', 1, false)"))
        con.commit()


@pytest.fixture
def test_todo():
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
