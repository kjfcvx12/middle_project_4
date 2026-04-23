from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from dotenv import load_dotenv

from app.db.database import Base, async_engine
#from app.middleware.token_refresh import RefreshTokenMiddleware


from app.routers import users, notes
from app.routers import boards, comments
from app.routers import gyms, gym_staffs,gym_machines
from app.routers import machines, parts
from app.routers import  routines,routine_details


load_dotenv(dotenv_path="../../.env")


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app=FastAPI(lifespan=lifespan)

#app.add_middleware(RefreshTokenMiddleware)


@app.get("/")
async def root():
    return {"message": "home"}

app.include_router(users.router)
app.include_router(notes.router)

app.include_router(boards.router)
app.include_router(comments.router)

app.include_router(machines.router)
app.include_router(parts.router)

app.include_router(gyms.router)
app.include_router(gym_staffs.router)
app.include_router(gym_machines.router)

app.include_router(routines.router)
app.include_router(routine_details.router)





#uvicorn main:app --port=8081 --reload
