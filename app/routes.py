from typing import List
from fastapi import Depends, APIRouter
from app.logic import (
    create_game,
    get_all_games,
    search_games,
    get_random_games,
    get_game_by_id,
    update_game_by_id,
    delete_game_by_id,
    filter,
)

#db imports
from sqlalchemy.orm import Session
from app.models import GameCreate, GameResponse, GameUpdate
from app.database import get_db

router = APIRouter()

# add new game (POST)
@router.post("/games", response_model=GameResponse)
async def add_game(game: GameCreate, db: Session = Depends(get_db)):
    # check for existing game with same name and platform
   return create_game(game, db)

# return all games
@router.get("/games", response_model=List[GameResponse])
async def get_games(db: Session = Depends(get_db)):
    return get_all_games(db)

# search for a game based on keyword
@router.get("/games/search", response_model=List[GameResponse])
async def search(q: str, db: Session = Depends(get_db)):
    return search_games(q, db)

# generate a random game suggestion
@router.get("/games/random", response_model=GameResponse)
async def get_random(db: Session = Depends(get_db)):
    return get_random_games(db)

# info about specific game
@router.get("/games/{game_id}", response_model=GameResponse)
async def get_specific_game(game_id: int, db: Session = Depends(get_db)):
    return get_game_by_id(game_id, db)

# update game (PUT)
@router.put("/games/{game_id}", response_model=GameResponse)
async def update_game(game_id: int, game_update: GameUpdate, db: Session = Depends(get_db)) -> int:
    return update_game_by_id(game_id, game_update, db)


# delete game (DELETE)
@router.delete("/games/{game_id}", response_model=GameResponse)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    return delete_game_by_id(game_id, db)

# filter by platform (GET)
@router.get("/games/platform/{platform}", response_model=list[GameResponse])
async def filter_by_platform(platform: str, db: Session = Depends(get_db)):
    return filter(platform, db)