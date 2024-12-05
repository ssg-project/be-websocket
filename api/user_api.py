from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.user_service import UserService
from ..dto.dto import *
from ..utils.database import get_db

router = APIRouter(prefix='/auth', tags=['user'])

@router.login('/login', description='로그인')
async def login(
    request: UserLoginReqeust,
    db: Session = Depends(get_db),
):
    user_service = UserService(db)

    try:
        user = user_service.get_user_by_email(email=request.email)
        if user.password == request.password:
            return
        else:
            raise HTTPException(status_code=401, detail="로그인 실패")
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)


@router.post('/join', description='회원 가입')
async def join(
    request: UserJoinRequest,
    db: Session = Depends(get_db),
):
    user_service = UserService(db)

    try:
        user_service.insert_db_user(email=request.email, password=request.password)
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    
@router.post('/withdrawal', description='회원 탈퇴')
async def withdrawal(
    request: UserDeleteRequest,
    db: Session = Depends(get_db),
):
    user_service = UserService(db)

    try:
        user_service.delete_db_user(id=request.user_id)
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
