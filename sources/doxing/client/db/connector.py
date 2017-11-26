from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from doxing.client.db.model import Base, Document
from doxing.client.document_dto import DocumentDTO

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


def parse_to_document(func):
    def wrapped(*args, **kwargs):
        ret = func(*args, **kwargs)
        try:
            return [DocumentDTO.from_local_db_object(i) for i in ret]
        except TypeError:
            return DocumentDTO.from_local_db_object(ret)

    return wrapped


class DocumentDao(Dao):
    @parse_to_document
    def list(self):
        """
        :rtype: [doxing.client.db.model.Document]
        """
        with DatabaseConnector() as db:
            return db.session.query(Document).all()

    def add(self, name, content):
        with DatabaseConnector() as db:
            document = Document(name=name, content=content)
            db.session.add(document)
            db.session.commit()
            db.session.refresh(document)

            return document.document_id

    def update(self, document_id, name=None, content=None):
        with DatabaseConnector() as db:
            document = db.session.query(Document).filter(Document.document_id == document_id).first()
            if name is not None:
                document.name = name

            if content is not None:
                document.content = content

            db.session.commit()
