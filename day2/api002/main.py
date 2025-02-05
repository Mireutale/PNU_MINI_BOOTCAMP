from fastapi import FastAPI
from app.handlers import auth_handlers, posts_handlers

app = FastAPI()

app.include_router(auth_handlers.router)
app.include_router(posts_handlers.router)