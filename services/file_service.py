from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user_model import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func

class FileService:
    def __init__(self, db: Session):
        self.db = db