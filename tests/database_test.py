from fastapi.testclient import TestClient
from app.app import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database.database import get_db,Base
import os
from dotenv import load_dotenv
load_dotenv()


database_url_test=os.getenv('database_url_test')

engine=create_engine(database_url_test)

TestingSessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False,expire_on_commit=False)



@pytest.fixture()
def session():
    TestingSessionLocal.close_all()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    except:
        db.close()



@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        except:
            session.close()
    app.dependency_overrides[get_db]=override_get_db           
    yield TestClient(app)
       