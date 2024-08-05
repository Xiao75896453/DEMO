from sqlalchemy import Column, DateTime, Integer, SmallInteger, String
from src.utils.db_connector import db


class Account(db.get_base()):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    failed_attempts = Column(SmallInteger, default=0, nullable=False)
    block_verification_time = Column(DateTime)
