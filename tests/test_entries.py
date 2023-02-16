from app.db.models.entries_model import Entries
from app.api.schemas.entries_schema import EntriesResponse


def test_get_all_entries(authorized_client,test_entries):
    res=authorized_client.get('/entries/')
    def validate(entry):
        return Entries(**entry)    
    map(validate,res.json())

    assert res.status_code == 200
    

def test_unauthorized_get_all_entries(client,test_entries):
    res=client.get('/entries/')
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'
    

def test_get_single_entry(authorized_client,test_entries,id=2):
    res=authorized_client.get(f'/entries/{id}')

    entry=EntriesResponse(**res.json())
    assert res.status_code == 200
    assert entry.id== id
    
def test_unauthorized_get_single_entry(client,test_entries):
    res=client.get('/entries/1')
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'

def test_get_single_entry_not_found(authorized_client,test_entries,id=100):
    res=authorized_client.get(f'/entries/{id}')
   
    assert res.status_code == 404
    assert res.json()['detail'] == 'There is no resource wiith the id 100'

def test_create_entry(authorized_client,test_entries):
    res=authorized_client.post('/entries',json={'title':'my test title','body':'my test body'})
    entry=EntriesResponse(**res.json())
    assert res.status_code ==201
    assert entry.title == 'my test title'
    assert entry.body =='my test body'

def test_unauthorized_test_create_entry(client,test_entries):
    res=client.post('/entries',json={'title':'my test title','body':'my test body'})
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'

def test_update_entry(authorized_client,test_entries):
    res=authorized_client.put('/entries/1',json={'title':'my test title','body':'my test body'})
    assert res.status_code == 200
    assert res.json() == 'updated'


def test_unauthorized_update_entry(client,test_entries):
    res=client.put('/entries/1',json={'title':'my test title','body':'my test body'})
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'

def test_update_entry_not_found(authorized_client,test_entries):
    res=authorized_client.put('/entries/100',json={'title':'my test title','body':'my test body'})
    
    assert res.status_code == 404
    assert res.json()['detail'] == 'There is no resource wiith the id 100'

def test_delete_entry(authorized_client,test_entries):
    res=authorized_client.delete('/entries/1')
    
    assert res.status_code==200
    assert res.json()=='entry has been deleted'

def test_unauthorized_delete_entry(client,test_entries):
    res=client.delete('/entries/1')
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'

def test_delete_entry_not_found(authorized_client,test_entries):
    res=authorized_client.delete('/entries/100')
    assert res.status_code == 404
    assert res.json()['detail'] == 'There is no resource wiith the id 100'

 
