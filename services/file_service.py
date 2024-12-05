from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.file_model import File
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
import boto3
import os

class FileService:
    def __init__(self, db: Session):
        self.db = db

        self.s3_client = boto3.client(
            's3', 
            aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
            region_name='ap-northeast-1',
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        
    def upload_s3_file(self, file_name: str, file_content: bytes):
        try:
            s3_response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_content
            )
            
            if s3_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return f'https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{file_name}'
            else:
                raise RuntimeError("S3 error")
        except Exception as e:
            raise Exception(f"S3 error: {str(e)}")

    def delete_s3_files(self, file_names: list[str]):
        s3_objects = [{'Key': file_name} for file_name in file_names]

        try:
            self.s3_client.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    'Objects': s3_objects,
                    'Quiet': True
                }
            )
            return
        except Exception as e:
            raise Exception(f"S3 error: {str(e)}")

    def insert_db_file(self, user_id: int, key: str, file_url: str):
        try:
            new_file = File(
                user_id=user_id,
                key=key,
                file_url=file_url,
            )
            self.db.add(new_file)
            self.db.commit()
            self.db.refresh(new_file)

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
    