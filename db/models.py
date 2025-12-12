from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from db.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    file_path = Column(String)
    file_size = Column(Float)
    file_type = Column(String)
    uploaded_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<File(id={self.id}, filename={self.original_filename}, size={self.file_size})>"
