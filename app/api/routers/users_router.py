from fastapi import APIRouter,status,Depends,HTTPException
from app.api.schemas.users_schema import UserRequest,UserResponse,LoginResponse,Token,TokenUserResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.users_model import User
from app.common.hashing import Hash
from app.api.dependency import get_current_user




router = APIRouter(tags=['users'],prefix='/users')


@router.post('/register',response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def create(request:UserRequest,db:Session=Depends(get_db)):

    user=db.query(User).filter(User.email==request.email).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'A user account with the email :{request.email} already exist')

    new_user= User(username=request.username,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = new_user.create_access_token(
        data={
            "user_id": new_user.id,
            } 
    )

    response={
        'username':new_user.username,
        'email':new_user.email,
        'id':new_user.id,
        'token':{ 
            "access_token": access_token,
            "token_type": "Bearer",
            }
        }
    return response


@router.post('/login',response_model=Token,status_code=status.HTTP_200_OK)
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==request.username).first()

    if not user:
        raise HTTPException(status_code=404, detail = f'user with the email :{request.username} was not found')

    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Invalid Credentials')

    access_token = user.create_access_token(
        data={"user_id": user.id} 
    )

    data={ 
            "access_token": access_token,
            "token_type": "Bearer",
            }
    return data

@router.post('/user',status_code=status.HTTP_200_OK,response_model=TokenUserResponse)
def get_user(request:Token,db:Session=Depends(get_db)):
    token=request.access_token
    
    id=get_current_user(token)
    
    user=db.query(User).filter(User.id==id.user_id).first()

    return user


