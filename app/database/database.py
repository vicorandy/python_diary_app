from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,declarative_base,scoped_session
import os
from dotenv import load_dotenv
load_dotenv()

database_url = os.getenv('database_url')

engine=create_engine(database_url,pool_size=50,echo=False)

SessionLocal=scoped_session(sessionmaker(bind=engine,autocommit=False,autoflush=False,expire_on_commit=False))


Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    except:
        db.close()
       
