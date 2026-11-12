from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import sessionmaker
from database import Base
from repositories.admin_repositories import AdminRepository
from repositories.user_repositories import UserRepository
import pytest
import sys
import os


TEST_DB = "sqlite:///:memory:"

@pytest.fixture(scope='function')
def test_session():
    engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def admin_repo(test_session):
    return AdminRepository(test_session)

@pytest.fixture
def user_repo(test_session):
    return UserRepository(test_session)