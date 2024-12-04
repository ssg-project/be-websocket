from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True, index=True)
    storage_id = Column(BigInteger, ForeignKey("storages.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    storage = relationship("Storage", back_populates="files")