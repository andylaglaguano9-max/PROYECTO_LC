from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import users
from app.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users API", description="CRUD de usuarios con FastAPI + PostgreSQL", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
