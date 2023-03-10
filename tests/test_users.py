import pytest
from app.api.schemas.users_schema import UserResponse ,Token,TokenUserResponse
from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv("ALGORITHM")




    
def test_login_user(new_user,client):
    user=new_user
    res=client.post('/users/login',data={"username":user['email'],"password":user['password']})
    token=Token(**res.json())
    payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id=payload.get('user_id')
    assert id == user['id']
    assert res.status_code == 200
    
def test_incorrect_login(new_user,client):
  
   res = client.post('/users/login',data={"username":"test_user@gmail.com","password":"wrong_password"})
   assert res.status_code ==401
   assert res.json()['detail'] == 'Invalid Credentials'

def test_no_user_login(client):
   res = client.post('/users/login',data={"username":"test_user@gmail.com","password":"wrong_password"})
   assert res.status_code ==404
   assert res.json()['detail'] == 'user with the email :test_user@gmail.com was not found'
   
 

def test_create_user(client):
    res=client.post('/users/register',json={"username":"test","email":"test@gmail.com","password":"testpassword"})
    new_user =UserResponse(**res.json())
    assert new_user.email=='test@gmail.com'
    assert new_user.username=='test'


def test_create_user_already_exist(new_user,client):
    res=client.post('/users/register',json={"username":"test_user","email":"test_user@gmail.com","password":"test_user_password"})
    assert res.status_code == 400
    assert res.json()['detail']=='A user account with the email :test_user@gmail.com already exist'

def test_get_user(new_user,client):
    data=new_user['token']
    token=data['access_token']
    res=client.post('/users/user',json={'access_token':token, 'token_type': 'Bearer'})
    user=TokenUserResponse(**res.json())
    assert new_user['username'] == user.username
    assert new_user['id'] == user.id
    assert new_user['email'] == user.email
    assert res.status_code == 200


def test_rooter(client):
    res=client.get('/')
    assert res.json().get('message') == 'welcome your server is live'
    assert res.status_code == 200

