from fastapi import APIRouter,Depends,HTTPException,status
from .entries_schema import EntriesRequest,EntriesResponse
from app.database.database import get_db
from sqlalchemy.orm import Session
from .entries_model import Entries
from app.component.users.users_schema import UserRequest


def post_entry(request:EntriesRequest,current_user:UserRequest,db:Session=Depends(get_db)):
    user_id=current_user.user_id
    new_entry =Entries(user_id=user_id,title=request.title,body=request.body)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def fetch_all_entries(current_user:UserRequest,db:Session=Depends(get_db)):
    user_id=current_user.user_id
    entries=db.query(Entries).filter(Entries.user_id==user_id).all()
    return entries
    
def fetch_entry(id,current_user:UserRequest,db:Session=Depends(get_db)):
    user_id=current_user.user_id
    entry=db.query(Entries).filter(Entries.id==id).first()
    
    if not entry :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no resource wiith the id {id}')
    
    if user_id !=entry.user_id :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to access this resource')

    return entry

def update_entry(id,request:EntriesRequest,current_user:UserRequest,db:Session=Depends(get_db)):
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


def remove_entry(id,current_user:UserRequest,db:Session=Depends(get_db)):

    user_id=current_user.user_id

    entry=db.query(Entries).filter(Entries.id==id).first()

    if not entry :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no resource wiith the id {id}')
    
    if user_id !=entry.user_id :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='You are not authorized to access this resource')
    
    db.query(Entries).filter(Entries.id==id).delete(synchronize_session=False)

    db.commit()

    return 'entry has been deleted'