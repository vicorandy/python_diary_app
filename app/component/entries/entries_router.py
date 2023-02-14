from fastapi import APIRouter,Depends,status
from typing import List
from .entries_schema import EntriesRequest,EntriesResponse
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.middel_ware.auth import get_current_user
from app.component.users.users_schema import UserRequest
from .entries_controller import post_entry,fetch_all_entries,fetch_entry,update_entry,remove_entry


router = APIRouter(prefix='/entries',tags=['Entries'])

@router.get('/',response_model=List[EntriesResponse],status_code=status.HTTP_200_OK)
def get_all_entries(current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
    return fetch_all_entries(current_user,db)

@router.get('/{id}',response_model=EntriesResponse,status_code=status.HTTP_200_OK)
def get_entry(id:int,current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
    return fetch_entry(id,current_user,db)

@router.post('/',response_model=EntriesResponse,status_code=status.HTTP_201_CREATED)
def create_entry(request:EntriesRequest,current_user:UserRequest=Depends(get_current_user), db:Session=Depends(get_db)):
    return post_entry(request,current_user,db)

@router.put('/{id}',status_code=status.HTTP_200_OK)
def edit_entry(id:int,request:EntriesRequest,current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
    return update_entry(id,request,current_user,db)

@router.delete('/{id}',status_code=status.HTTP_200_OK)
def delete_entry(id,current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
    return remove_entry(id,current_user,db)