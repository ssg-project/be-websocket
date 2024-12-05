from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..services.file_service import FileService
from ..services.user_service import UserService
from ..dto.dto import *
from ..utils.database import get_db
import asyncio

router = APIRouter(prefix='/file', tags=['file'])

@router.post('/upload', description='파일 업로드')
async def upload_files(
    request: Request,
    request_body: List[FileUploadRequest],
    db: Session = Depends(get_db),
):
    file_service = FileService(db)

    try:
        file_list = []
                
        try:
            # S3 업로드 병렬 처리
            results = await asyncio.gather(
                *(file_service.upload_s3_file(
                    file_name=file.file_name,
                    file_content=file.file_content,
                   ) for file in request_body
                ),
                return_exceptions=True
            )

            # 성공한 파일만 필터링
            user_id = request.session.get('user_id')
            user_email = request.session.get('user_email')

            for result in results:
                if isinstance(result, dict):
                    file_list.append({
                        "user_id": user_id,
                        "key": f"{user_email}/{result['file_name']}",
                        "file_url": result["file_url"]
                    })

            # DB에 파일 정보 저장
            if file_list:
                file_service.insert_db_files(file_list)

            return

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")        
                
                
        # db insert
        file_key = f'{request.session.get('user_email')}/{request_body.file_name}'
        
        file_service.insert_db_file(
            user_id=request.session.get('user_email'),
            key=file_key,
            file_url=file_url
        )

        return    
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    
@router.post('/delete', description='파일 삭제')
def delete_file(
    request: Request,
    request_body: FileDeleteRequest,
    db: Session = Depends(get_db),
):
    file_service = FileService(db)

    try:
        # db get files
        files = file_service.get_files_by_file_ids(
            user_id=request.session.get('user_id'),
            file_ids=request_body.file_ids,
        )
        file_names = [i['key'] for i in files]
        
        # db delete
        file_service.delete_db_file(file_ids=request_body.file_ids)

        # s3 file delete
        file_service.delete_s3_files(file_names=file_names)

        return    
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    
@router.get('/list', response_model=GetFileListResponse, description='파일 리스트 조회')
def get_files(
    request: Request,
    db: Session = Depends(get_db),
):
    file_service = FileService(db)

    try:
        # db get files
        files = file_service.get_files(user_id=request.session.get('user_id'))
        response_files = [file.to_dict() for file in files]

        return GetFileListResponse(files=response_files)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)