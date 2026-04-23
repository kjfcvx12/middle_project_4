from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.db.database import Base, async_engine
from app.routers import boards, comments, users
#from app.routers import users
#from app.middleware.token_refresh import RefreshTokenMiddleware


load_dotenv(dotenv_path="../../.env")


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app=FastAPI(lifespan=lifespan)

#app.add_middleware(RefreshTokenMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "home"}

#app.include_router(users.router)
app.include_router(boards.router)
app.include_router(comments.router)
app.include_router(users.router)


#uvicorn main:app --port=8081 --reload
