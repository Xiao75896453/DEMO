from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from lib.db_engine.db_interface import DBInterface


@dataclass
class DBUrlParameter:
    driver_name: str
    user: str
    password: str
    host: str
    port: int
    database: str
    driver: str | None = None


@dataclass
class DBConnectionParameter:
    pool_size: int
    max_overflow: int
    pool_recycle: int


class SqlAlchemy(DBInterface):
    def __init__(
        self,
        db_url_parameter: DBUrlParameter,
        db_connection_parameter: DBConnectionParameter,
    ) -> None:
        # create a SQLAlchemy "engine"
        self.__set_db_rul(db_url_parameter)

        self.__engine = create_engine(
            self.__db_url,
            pool_size=db_connection_parameter.pool_size,
            max_overflow=db_connection_parameter.max_overflow,
            pool_recycle=db_connection_parameter.pool_recycle,
        )
        # Later we will inherit from this class to create each of the database models or classes
        # (the ORM models)
        self.__base = declarative_base()

        # Each instance of the SessionLocal class will be a database session.
        # The class itself is not a database session yet.
        # But once we create an instance of the SessionLocal class,
        # this instance will be the actual database session.
        self.__session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.__engine
        )

        super().__init__(base=self.__base, engine=self.__engine)

    def __set_db_rul(self, db_url_parameter: DBUrlParameter) -> None:
        db_url = (
            rf"{db_url_parameter.driver_name}://"
            + f"{db_url_parameter.user}:{db_url_parameter.password}"
            + f"@{db_url_parameter.host}:{db_url_parameter.port}/{db_url_parameter.database}"
        )

        if db_url_parameter.driver:
            db_url += f"?driver={db_url_parameter.driver}"

        self.__db_url = db_url

    def get_db_url(self) -> str:
        return self.__db_url

    def create_db_session(self):
        return self.__session()

    def drop_all_tables(self) -> None:
        super().get_base().metadata.drop_all(bind=super().get_engine())
