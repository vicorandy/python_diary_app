from app.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,String,Integer,ForeignKey

class Entries (Base):
    __tablename__='entries'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)
    # user_id =Column(Integer, ForeignKey('users.id')) 

    
