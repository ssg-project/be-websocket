from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
# from models import 
import boto3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func


DATABASE_URL = "mysql+pymysql://root:root@localhost/storage_project"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    storage_id = Column(Integer, ForeignKey("storages.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    storage = relationship("Storage", back_populates="files")

class Storage(Base):
    __tablename__ = "storages"

    id = Column(Integer, primary_key=True, index=True)
    storage_name = Column(String(255), nullable=False)

    user = relationship("User", back_populates="storage", uselist=False, cascade="all, delete")
    files = relationship("File", back_populates="storage", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    storage_id = Column(Integer, ForeignKey("storages.id", ondelete="CASCADE"), unique=True)

    storage = relationship("Storage", back_populates="user", cascade="all, delete")
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class StorageService:
    def __init__(self, db: Session):
        self.db = db

        self.s3_client = boto3.client(
            's3', 
            aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')

    def upload_s3_file(self, file_name: str, file_content: bytes):
        try:
            s3_response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_content
            )
            return s3_response
        except Exception as e:
            raise Exception(f"Error during file upload to S3: {str(e)}")

    def delete_s3_file(self, file_name: str):
        try:
            s3_response = self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return s3_response
        except Exception as e:
            raise Exception(f"Error during file deletion from S3: {str(e)}")

    def insert_db_file(self, storage_id: int, file_name: str):
        try:
            new_file = File(
                storage_id=storage_id,
                file_name=file_name,
            )
            self.db.add(new_file)
            self.db.commit()
            self.db.refresh(new_file)

            print(new_file)
            return new_file

        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def delete_db_file(self, file_id: int):
        try:
            query = self.db.query(File).filter(File.id == file_id)

            file_to_delete = query.first()
            self.db.delete(file_to_delete)
            self.db.commit()

            print(f"File with ID {file_to_delete.id} and name '{file_to_delete.file_name}' deleted successfully.")
            return file_to_delete
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error during deletion: {str(e)}")
    
    def test(self):
        try:
            new_storage = Storage(
                storage_name="zz"                
            )
            self.db.add(new_storage)
            self.db.commit()
            self.db.refresh(new_storage)

            print(new_storage)
            return new_storage

        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def test2(self):
        try:
            new_user = User(
                email="zz",
                password="zz",
                storage_id=1,
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            print(new_user)
            return new_user

        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
if __name__ == "__main__":
    db_session = next(get_db())  # DB 세션을 얻습니다.
    
    # StorageService 객체에 세션을 전달
    service = StorageService(db_session)
    service.test2()
