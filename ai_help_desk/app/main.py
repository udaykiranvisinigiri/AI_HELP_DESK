from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.metrics import router as metrics_router
from app.api import auth

app = FastAPI()

app.include_router(chat_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
