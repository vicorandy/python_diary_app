from fastapi import APIRouter,Depends,status,HTTPException
from typing import List
from app.api.schemas.entries_schema import EntriesRequest,EntriesResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.api.dependency import get_current_user
from app.api.schemas.users_schema import UserRequest
from app.db.models.entries_model import Entries

router = APIRouter(prefix='/entries',tags=['Entries'])

@router.get('/',response_model=List[EntriesResponse],status_code=status.HTTP_200_OK)
def get_all_entries(current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
    user_id=current_user.user_id
    entries=db.query(Entries).filter(Entries.user_id==user_id).all()
    return entries

@router.get('/{id}',response_model=EntriesResponse,status_code=status.HTTP_200_OK)
def get_entry(id:int,current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
    user_id=current_user.user_id
    entry=db.query(Entries).filter(Entries.id==id).first()
    
    if not entry :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no resource wiith the id {id}')
    
    if user_id !=entry.user_id :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to access this resource')

    return entry

@router.post('/',response_model=EntriesResponse,status_code=status.HTTP_201_CREATED)
def create_entry(request:EntriesRequest,current_user:UserRequest=Depends(get_current_user), db:Session=Depends(get_db)):
   
    user_id=current_user.user_id
    new_entry =Entries(user_id=user_id,title=request.title,body=request.body)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put('/{id}',status_code=status.HTTP_200_OK)
def edit_entry(id:int,request:EntriesRequest,current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
    
    user_id=current_user.user_id
    title=request.title
    body=request.body
    entry=db.query(Entries).filter(Entries.id==id).first()

    if not entry :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no resource wiith the id {id}')
    
    if user_id !=entry.user_id :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to access this resource')
    
    db.query(Entries).filter(Entries.id==id).update({'title':title,'body':body})

    db.commit()

    return'updated'


@router.delete('/{id}',status_code=status.HTTP_200_OK)
def delete_entry(id,current_user:UserRequest=Depends(get_current_user),db:Session=Depends(get_db)):
  
    user_id=current_user.user_id

    entry=db.query(Entries).filter(Entries.id==id).first()

    if not entry :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no resource wiith the id {id}')
    
    if user_id !=entry.user_id :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to access this resource')
    
    db.query(Entries).filter(Entries.id==id).delete(synchronize_session=False)

    db.commit()

    return 'entry has been deleted'

