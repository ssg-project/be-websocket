from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.model import File
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
import aioboto3
import boto3
import os
from dotenv import load_dotenv

class FileService:
    def __init__(self, db: Session):
        load_dotenv()

        self.db = db
                        
        self.aws_access_key_id = os.getenv('S3_ACCESS_KEY')
        self.aws_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        self.region_name = os.getenv('S3_REGION_NAME')

        self.s3_client = boto3.client(
            's3', 
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )
        
    async def upload_s3_file(self, file_name: str, file_content: bytes):
        try:
            if not file_content:
                raise ValueError("File content is empty or invalid.")
            async with aioboto3.Session().client(
                's3', 
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name,
            ) as s3_client:
                s3_response = await s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_name,
                    Body=file_content
                )
                
                if s3_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return {
                        'file_name': file_name,
                        'file_url': f'https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{file_name}',
                    }
                else:
                    raise RuntimeError("S3 error")
        except Exception as e:
            raise Exception(f"S3 error: {str(e)}")

    def delete_s3_files(self, file_names: list[str]):
        s3_objects = [{'Key': file_name} for file_name in file_names]
        try:
            s3_response = self.s3_client.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    'Objects': s3_objects,
                    'Quiet': True
                }
            )
           
            if s3_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return
            else:
                raise RuntimeError("S3 error")
        except Exception as e:
            raise Exception(f"S3 error: {str(e)}")

    def insert_db_files(self, files: list[dict]):
        try:
            new_files = [File(user_id=file['user_id'], file_key=file['file_key'], file_url=file['file_url']) for file in files]

            self.db.add_all(new_files)
            self.db.commit()

            return new_files

        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def delete_db_files(self, file_ids: list[int]):
        try:
            query = self.db.query(File).filter(File.id.in_(file_ids))
            query.delete(synchronize_session=False)

            self.db.commit()
            return
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Database error during deletion: {str(e)}")
    
    def get_files(self, user_id: int):
        try:
            files = self.db.query(File).filter(File.user_id == user_id).all()
            files_to_dict = [file.to_dict() for file in files]
            return files_to_dict
        except SQLAlchemyError as e:
            raise Exception(f"Database error during deletion: {str(e)}")
        
    def get_files_by_file_ids(self, user_id: int, file_ids: list[int]):
        try:
            files = self.db.query(File).filter(
                File.user_id == user_id,
                File.id.in_(file_ids)
            ).all()
            files_to_dict = [file.to_dict() for file in files]
            return files_to_dict
        except SQLAlchemyError as e:
            raise Exception(f"Database error during deletion: {str(e)}")
