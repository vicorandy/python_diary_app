from  app.db.database import Base

from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import relationship

from datetime import datetime,timedelta
from jose import JWTError,jwt
from app.api.schemas.users_schema import TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String,unique=True)
    password=Column(String)
    
    
    def create_access_token(self,data:dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
  
    



