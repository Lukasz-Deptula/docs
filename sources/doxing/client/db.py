from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class DatabaseConnector(object):
    def __init__(self):
        super(DatabaseConnector, self).__init__()

        # TODO: read connection string
        self._connection_string = "sqlite:///doxing.db"

    def close(self):
        self.session.close()
        self.engine.dispose()

    def __enter__(self):
        self.engine = create_engine(self._connection_string, echo=False)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
        self.session.configure(bind=self.engine)
        self.session = self.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Dao(object):
    pass
