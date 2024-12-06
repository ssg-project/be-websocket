from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_key = Column(String(500), nullable=False)
    file_url = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="files")
    
    def to_dict(self):
        return {
            "id": self.id,
            "file_key": self.file_key,
            "file_url": self.file_url,
            "created_at": self.created_at,
        }
        
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    files = relationship("File", back_populates="user", cascade="all, delete-orphan")