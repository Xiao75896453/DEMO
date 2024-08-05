from sqlalchemy import Column, Integer, String
from src.utils.db_connector import db


class Account(db.get_base()):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
