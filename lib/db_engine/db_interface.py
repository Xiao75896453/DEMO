from abc import ABC, abstractmethod


class DBInterface(ABC):
    def __init__(self, base, engine) -> None:
        self.__base = base
        self.__engine = engine

    def get_db_session(self):
        db_session = self.create_db_session()

        try:
            yield db_session
        finally:
            db_session.close()

    @abstractmethod
    def create_db_session(self):
        pass

    def get_base(self):
        return self.__base

    def get_base_metadata(self):
        return self.__base.metadata

    def get_engine(self):
        return self.__engine
