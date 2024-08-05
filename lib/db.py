from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session


def init_tables(db_session: Session, tables: List[str]):
    for table in tables:
        db_session.execute(text("TRUNCATE " + table + " RESTART IDENTITY CASCADE;"))
        db_session.commit()
