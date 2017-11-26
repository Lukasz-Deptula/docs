class DocumentType:
    TEXT = "text"


class DocumentLocation:
    LOCAL_DB = "local_db"


class DocumentDTO(object):
    @classmethod
    def from_local_db_object(cls, db_object):
        """
        :type db_object: doxing.client.db.model.Document
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
