from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

### user
class UserLoginReqeust(BaseModel):
    email: str
    password: str

class UserJoinRequest(BaseModel):
    email: str
    password: str

class UserDeleteRequest(BaseModel):
    user_id: int

### file
class FileUploadRequest(BaseModel):
    key: str
    file_body: bytes
    
class FileDeleteRequest(BaseModel):
    file_names: List[str]

class GetFileListRequest(BaseModel):
    user_id: int

class FileItem(BaseModel):
    id: int
    user_id: int
    key: str
    file_url: str
    created_at: datetime
    updated_at: datetime
    
class GetFileListREponse(BaseModel):
    data: List[FileItem]
