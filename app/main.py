#info about the app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as game_router

app = FastAPI(
    title="Game Collection API", 
    version="0.1.0"
)

origins = [
    "http://localhost:5500",
    "localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(game_router)