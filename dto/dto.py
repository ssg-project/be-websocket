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
    file_name: str
    file_content: bytes
    
class FileDeleteRequest(BaseModel):
    file_ids: List[int]

class FileItem(BaseModel):
    id: int
    user_id: int
    key: str
    file_url: str
    created_at: datetime
    updated_at: datetime
    
class GetFileListResponse(BaseModel):
    data: List[FileItem]
