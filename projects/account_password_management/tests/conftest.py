import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from src.config.config import settings
from src.main import app
from src.utils.db_connector import db

from lib.db import init_tables


@pytest.fixture(scope="session", autouse=True)
def test_client():
    # When you need your event handlers (startup and shutdown) to run in your tests
    # https://fastapi.tiangolo.com/advanced/testing-events/
    with TestClient(app) as test_client_:
        yield test_client_


@pytest.fixture(scope="session")
def db_engine():
    db_engine_ = db.get_engine()

    yield db_engine_


@pytest.fixture(scope="session")
def init_db_schema(db_engine):
    db.get_base_metadata().drop_all(bind=db_engine)

    __db_migration()

    yield


def __db_migration():
    alembic_args = [
        "-c",
        f"{settings.PROJECT_PATH}/alembic.ini",
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembic_args)


@pytest.fixture(scope="session")
def db_session_factory():
    try:
        yield next(db.get_db_session())
    except StopIteration:
        print("db_session_factory fail")
        yield None


@pytest.fixture(scope="session")
def db_session(db_session_factory):
    db_session_ = db_session_factory

    yield db_session_

    db_session_.close()


@pytest.fixture(scope="function", autouse=True)
def init_db(db_session):

    yield

    # disables all foreign key checks,
    db_session.execute(text("SET session_replication_role = 'replica'"))
    init_tables(db_session=db_session, tables=db.get_base_metadata().tables.keys())
    # enables all foreign key checks,
    db_session.execute(text("SET session_replication_role = 'origin'"))
    db_session.commit()
