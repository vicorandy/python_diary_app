from pydantic import BaseModel
from typing import Optional
from pydantic import constr



class EntriesResponse(BaseModel):
    id:int
    title:str
    body:str
    user_id:int
    class Config():
        orm_mode=True

class EntriesRequest(BaseModel):
    title:constr(min_length=1)
    body:constr(min_length=1)
    user_id:Optional[str]= None

