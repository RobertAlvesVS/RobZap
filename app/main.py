from fastapi import FastAPI
from app.routers.webhook import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Funcionando"}
