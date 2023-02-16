from fastapi import FastAPI
from app.db.models import users_model,entries_model
from app.db.database import engine
from app.api import api

users_model.Base.metadata.create_all(engine)
entries_model.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(api.api_router)


@app.get('/')
def welcome():
    return{'message':'welcome your server is live'}


