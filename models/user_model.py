from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    storage_id = Column(Integer, ForeignKey("storages.id", ondelete="CASCADE"), unique=True)

    storage = relationship("Storage", back_populates="user", cascade="all, delete orphan")