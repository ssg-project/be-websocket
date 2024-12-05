from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(500), nullable=False)
    file_url = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="files")