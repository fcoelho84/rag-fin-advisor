from fastapi import FastAPI

from app.routers.extractor import router as extractorRoute

app = FastAPI()

app.include_router(extractorRoute)


@app.get("/")
async def read_root() -> str:
    return ["OK"]
