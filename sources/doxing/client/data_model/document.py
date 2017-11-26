from sqlalchemy import Column, Integer, String

from doxing.client.db import DatabaseConnector, Dao, Base


class DocumentDbModel(Base):
    __tablename__ = "documents"
    document_id = Column("document_id", Integer, primary_key=True)
    name = Column("name", String)
    content = Column("content", String)


class DocumentDTO(object):
    @classmethod
    def from_local_db_object(cls, db_object):
        """
        :type db_object: doxing.client.data_model.document.DocumentDbModel
        :rtype: DocumentDTO
        """
        dto = cls()
        # TODO: shall be read from db
        dto.type = DocumentType.TEXT
        dto.name = db_object.name
        dto.storage_type = DocumentLocation.LOCAL_DB
        dto.content = db_object.content
        dto.location = db_object.document_id
        return dto

    def __init__(self):
        # TODO: so far it's only one supported
        self.type = DocumentType.TEXT

        # TODO: so far it's only one supported
        self.storage_type = DocumentLocation.LOCAL_DB

        self.location = None
        self.name = ""
        self.content = None

    def save(self):
        if self.storage_type == DocumentLocation.LOCAL_DB:
            if self.location is None:
                self._save_to_local_db()
            else:
                self._update_in_local_db()
        else:
            raise RuntimeError("Not supported storage type {}".format(self.storage_type))

    def _save_to_local_db(self):
        self.location = DocumentDao().add(name=self.name, content=self.content)

    def _update_in_local_db(self):
        DocumentDao().update(self.location, name=self.name, content=self.content)


class DocumentType:
    TEXT = "text"


class DocumentLocation:
    LOCAL_DB = "local_db"


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
        :rtype: [doxing.client.db.model.DocumentDbModel]
        """
        with DatabaseConnector() as db:
            return db.session.query(DocumentDbModel).all()

    def add(self, name, content):
        with DatabaseConnector() as db:
            document = DocumentDbModel(name=name, content=content)
            db.session.add(document)
            db.session.commit()
            db.session.refresh(document)

            return document.document_id

    def update(self, document_id, name=None, content=None):
        with DatabaseConnector() as db:
            document = db.session.query(DocumentDbModel).filter(DocumentDbModel.document_id == document_id).first()
            if name is not None:
                document.name = name

            if content is not None:
                document.content = content

            db.session.commit()
