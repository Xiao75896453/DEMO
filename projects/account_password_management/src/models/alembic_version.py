from sqlalchemy import Column, String
from src.utils.db_connector import db


# pylint: disable=too-few-public-methods
class AlembicVersion(
    db.get_base()
):  # for pytest conftest init_db_schema to drop alembic_version table
    __tablename__ = "alembic_version"

    version_num = Column(String(32), primary_key=True, nullable=False)
