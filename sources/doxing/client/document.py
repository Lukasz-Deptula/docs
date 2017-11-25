class DocumentType:
    TEXT = "text"


class DocumentLocation:
    LOCAL_DB = "local_db"


class Document(object):
    def __init__(self):
        # TODO: so far it's only one supported
        self.type = DocumentType.TEXT

        # TODO: so far it's only one supported
        self.storage_type = DocumentLocation.LOCAL_DB

        self.name = ""

        self.content = None
