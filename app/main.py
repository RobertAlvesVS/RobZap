import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.webhook import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("temp_media", exist_ok=True)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/temp_media", StaticFiles(directory="temp_media"), name="temp_media")
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Funcionando"}
