from fastapi import FastAPI

from app.routers.analyze import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def read_root() -> str:
    return "UP"
