from typing import List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import random

#db imports
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
import sqlalchemy.orm
from sqlmodel import SQLModel, Field, create_engine

load_dotenv()

#info about the app
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

# database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# database model
class Game(SQLModel, table=True):
    __tablename__ = "games"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    platform: str

# create tables
SQLModel.metadata.create_all(bind=engine)

# dependency to get db session
def get_db():
    with Session(engine) as session:
        yield session

# pydantic model for request data
class GameCreate(SQLModel):
    name: str
    platform: str

# pydantic model for updating data
class GameUpdate(SQLModel):
    name: str
    platform: str

# pydantic model for response data
class GameResponse(SQLModel):
    id: int
    name: str
    platform: str

# add new game (POST)
@app.post("/games", response_model=GameResponse)
async def add_game(game: GameCreate, db: Session = Depends(get_db)):
    # check for existing game with same name and platform
    existing_game = db.query(Game).filter(
        Game.name == game.name,
        Game.platform == game.platform
    ).first()
    
    if existing_game:
        raise HTTPException(status_code=400, detail="Game already exists.")

    db_game = Game(**game.model_dump())
    
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

# return all games
@app.get("/games", response_model=List[GameResponse])
async def get_games(request: Request, db: Session = Depends(get_db)):
    db_games = db.query(Game).all()
    return db_games

# search for a game based on keyword
@app.get("/games/search", response_model=List[GameResponse])
async def search(q: str, db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.name.ilike(f"%{q}%")).all()

    if not db_game:
            raise HTTPException(status_code=404, detail="No games found.")
    
    return db_game

# generate a random game suggestion
@app.get("/games/random", response_model=GameResponse)
async def get_random(db: Session = Depends(get_db)):
    db_game = db.query(Game).all()

    if not db_game:
        raise HTTPException(status_code=404, detail="No games available!")

    random_game = random.choice(db_game)

    return random_game

# info about specific game
@app.get("/games/{game_id}", response_model=GameResponse)
async def get_specific_game(game_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Game).filter(Game.id == game_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_item

# update game (PUT)
@app.put("/games/{game_id}", response_model=GameResponse)
async def update_game(game_id: int, game_update: GameUpdate, db: Session = Depends(get_db)) -> int:
    db_game = db.query(Game).filter(Game.id == game_id).first()
    
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db_game.name = game_update.name
    db_game.platform = game_update.platform

    db.commit()
    db.refresh(db_game)
    
    return db_game


# delete game (DELETE)
@app.delete("/games/{game_id}", response_model=GameResponse)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(db_game)
    db.commit()
    
    return db_game

# filter by platform (GET)
@app.get("/games/platform/{platform}", response_model=list[GameResponse])
async def filter_by_platform(platform: str, db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.platform==platform).all()

    if not db_game:
            raise HTTPException(status_code=404, detail="No games under that platform")
    
    return db_game