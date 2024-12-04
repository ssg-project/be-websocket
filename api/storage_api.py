from fastapi import APIRouter

router = APIRouter(prefix='/storage', tags=['storage'])

@router.get("/upload") # response_model 추가
async def upload_file(): # dto: dto, db: Session = Depends(get_db) 추가
    return