from fastapi import Depends,HTTPException,status
from jose import jwt,JWTError 
from fastapi.security import OAuth2PasswordBearer 
from app.api.schemas.users_schema import TokenData
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='users/login')

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data: int = payload.get("user_id") 
        if data is None:
            raise credentials_exception
        token_data = TokenData(user_id=data)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token,credentials_exception)