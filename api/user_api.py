from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from services.user_service import UserService
from dto.dto import *
from utils.database import get_db

router = APIRouter(prefix='/auth', tags=['user'])

@router.post('/login', description='로그인')
def login(
    request: Request,
    request_body: UserLoginReqeust,
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    print(request_body)

    try:
        user = user_service.get_user_by_email(email=request_body.email)
        if user.password == request_body.password:
            request.cookies['user_id'] = user.id
            request.cookies['user_email'] = user.email
            
            return {'user_id': user.id, 'user_email': user.email}
        else:
            raise HTTPException(status_code=401, detail="로그인 실패")
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@router.post('/logout', description='로그아웃')
def logout(
    request: Request,
):
    try:
        del request.cookies['user_id']
        del request.cookies['user_email']
        
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@router.post('/join', description='회원 가입')
def join(
    request_body: UserJoinRequest,
    db: Session = Depends(get_db),
):
    user_service = UserService(db)

    try:
        user_service.insert_db_user(email=request_body.email, password=request_body.password)
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    
@router.post('/withdrawal', description='회원 탈퇴')
def withdrawal(
    request_body: UserDeleteRequest,
    db: Session = Depends(get_db),
):
    user_service = UserService(db)

    try:
        user_service.delete_db_user(id=request_body.user_id)
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
