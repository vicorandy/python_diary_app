from fastapi import APIRouter
from app.api.routers import users_router,entries_router

api_router =APIRouter()
api_router.include_router(users_router.router)
api_router.include_router(entries_router.router)

