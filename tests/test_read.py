# tests/test_crud_read.py
import pytest
from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ConfigDict
from alchemy_crud.functions.read import get_one, get_many
from alchemy_crud.helper import build_filter, _apply_order, _apply_pagination
from alchemy_crud.models.query import FindManyRequestData, PaginationData

Base = declarative_base()

# --- Simple SQLAlchemy User model ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Simple Pydantic read schema ---
class UserReadSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    username: str
    email: str
    age: int

# --- Pytest fixtures ---
@pytest.fixture(scope="module")
def engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    # Clear table before seeding
    session.query(User).delete()
    now = datetime.now(tz=timezone.utc)
    users = [
        User(username="alice", email="alice@example.com", age=25, created_at=now - timedelta(days=2)),
        User(username="bob", email="bob@example.com", age=30, created_at=now - timedelta(days=1)),
        User(username="carol", email="carol@example.com", age=22, created_at=now),
    ]
    session.add_all(users)
    session.commit()
    yield session
    session.close()


# --- Tests ---
def test_get_one_by_username(session: Session):
    filters = {"username": "alice"}
    user = get_one(session, User, filters, UserReadSchema)
    assert user.username == "alice"
    assert isinstance(user.id, int)

def test_get_many_with_age_filter(session: Session):
    filters = {"age": {"gte": 25}}
    users, total, pages = get_many(session, User, filters, UserReadSchema)
    assert len(users) == 2
    assert total == 2
    usernames = [u.username for u in users]
    assert "alice" in usernames and "bob" in usernames

def test_get_many_with_or_filter(session: Session):
    filters = {
        "username": {"neq": "alice"},
        "or_": [
            {"age": {"gt": 25}},
            {"age": {"lt": 23}}
        ]
    }
    users, total, pages = get_many(session, User, filters, UserReadSchema)
    usernames = [u.username for u in users]
    assert "alice" not in usernames
    assert total == 2

def test_get_many_order_by(session: Session):
    filters = {}
    # Apply ordering manually since _apply_order is used internally
    users, total, pages = get_many(session, User, filters, UserReadSchema, req=FindManyRequestData(
        order_by={"column": "age", "direction": "desc"}
    ))
    ages = [u.age for u in users]
    assert ages == sorted(ages, reverse=True)

def test_get_many_with_pagination(session: Session):
    
    filters = {}
    users, total, pages = get_many(session, User, filters, UserReadSchema, req=FindManyRequestData(
        pagination=PaginationData(limit=2, page=2)
    ))
    assert len(users) == 1  # Only 3 users total, second page has 1
    assert pages == 2
    assert total == 3

def test_get_one_not_found(session: Session):
    filters = {"username": "nonexistent"}
    user = get_one(session, User, filters, UserReadSchema)
    assert user is None
