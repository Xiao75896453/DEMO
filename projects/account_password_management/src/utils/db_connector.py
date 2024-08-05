from src.config.config import settings

from lib.db_engine.sqlalchemy import (DBConnectionParameter, DBUrlParameter,
                                      SqlAlchemy)

POSTGRESQL_DRIVER_NAME = "postgresql+psycopg2"

postgresql_url_parameter = DBUrlParameter(
    driver_name=POSTGRESQL_DRIVER_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_DATABASE,
)

db_connection_parameter = DBConnectionParameter(
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
)

db = SqlAlchemy(
    db_url_parameter=postgresql_url_parameter,
    db_connection_parameter=db_connection_parameter,
)
