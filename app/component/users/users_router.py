from fastapi import APIRouter,status,Depends
from .users_schema import UserRequest,UserResponse,LoginResponse,Token,TokenUserResponse
from .users_controller import create_user,login_user,fetch_user
from sqlalchemy.orm import Session 
from app.database.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['users'],prefix='/users')


@router.post('/register',response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def create(request:UserRequest,db:Session=Depends(get_db)):
    return create_user(request,db)


@router.post('/login',response_model=Token,status_code=status.HTTP_200_OK)
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return login_user(request,db)

@router.post('/user',status_code=status.HTTP_200_OK,response_model=TokenUserResponse)
def get_user(request:Token,db:Session=Depends(get_db)):
    
    return fetch_user(request,db)

