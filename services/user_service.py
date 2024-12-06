from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.model import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def insert_db_user(self, email: str, password: str):
        try:
            new_user = User(
                email=email,
                password=password,
            )

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            return new_user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def delete_db_user(self, user_id: int):
        try:
            query = self.db.query(User).filter(User.id == user_id)
            user_to_delete = query.first()

            self.db.delete(user_to_delete)
            self.db.commit()

            return user_to_delete
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def get_user_by_id(self, user_id: int):
        try:
            query = self.db.query(User).filter(User.id == user_id)
            user = query.first()
                        
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")

    def get_user_by_email(self, email: str):
        try:
            query = self.db.query(User).filter(User.email == email)
            user = query.first()
                        
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
        
if __name__ == '__main__':
    from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, TIMESTAMP, func
    from sqlalchemy.orm import relationship, declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = "users"

        id = Column(BigInteger, primary_key=True, autoincrement=True)
        email = Column(String(255), unique=True, nullable=False)
        password = Column(String(255), nullable=False)
        created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

        files = relationship("File", back_populates="user", cascade="all, delete-orphan")
    
    class File(Base):
        __tablename__ = "files"

        id = Column(BigInteger, primary_key=True, autoincrement=True)
        user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
        file_key = Column(String(500), nullable=False)
        file_url = Column(String(2048), nullable=False)
        created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

        user = relationship("User", back_populates="files")
    
    new_user = User(email='a', password='b')