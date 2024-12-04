from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Storage(Base):
    __tablename__ = "storages"

    id = Column(Integer, primary_key=True, index=True)
    storage_name = Column(String(255), nullable=False)

    user = relationship("User", back_populates="storage", uselist=False, cascade="all, delete")
    files = relationship("File", back_populates="storage", cascade="all, delete-orphan")
