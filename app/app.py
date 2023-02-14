from fastapi import FastAPI
from app.component.users import users_router,users_model
from app.component.entries import entries_router,entries_model
# from component.users import users_router,users_model
from app.database.database import engine

users_model.Base.metadata.create_all(engine)
entries_model.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(users_router.router)
app.include_router(entries_router.router)


@app.get('/')
def welcome():
    return{'message':'welcome your server is live'}


