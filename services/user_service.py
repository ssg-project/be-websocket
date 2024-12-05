from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user_model import User
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
    
    def get_user(self, user_id: int):
        try:
            query = self.db.query(User).filter(User.id == user_id)
            user = query.first()
                        
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
