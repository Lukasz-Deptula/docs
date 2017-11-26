from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    document_id = Column("document_id", Integer, primary_key=True)
    name = Column("name", String)
    content = Column("content", String)

