#info about the app
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as game_router

app = FastAPI(
    title="Game Collection API", 
    version="0.1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "https://custom-api-server-64rw.onrender.com",
    "http://localhost:5500",
    "localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://custom-api-server-64rw.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(game_router)