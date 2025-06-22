from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
import random
from app.models import Game, GameCreate, GameUpdate

def create_game(game: GameCreate, db: Session) -> Game:
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

def get_all_games(db: Session) -> List[Game]:
    """return all games"""
    return db.query(Game).all()

# search for a game based on keyword
def search_games(q: str, db: Session) -> List[Game]:
    games = db.query(Game).filter(Game.name.ilike(f"%{q}%")).all()

    if not games:
            raise HTTPException(status_code=404, detail="No games found.")
    
    return games

# generate a random game suggestion
def get_random_games(db: Session) -> Game:
    db_game = db.query(Game).all()

    if not db_game:
        raise HTTPException(status_code=404, detail="No games available!")

    random_game = random.choice(db_game)

    return random_game

# info about specific game
def get_game_by_id(game_id: int, db: Session) -> Game:
    game = db.query(Game).filter(Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

# update game
def update_game_by_id(game_id: int, game_update: GameUpdate, db: Session) -> Game:
    db_game = db.query(Game).filter(Game.id == game_id).first()
    
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db_game.name = game_update.name
    db_game.platform = game_update.platform

    db.commit()
    db.refresh(db_game)
    
    return db_game


# delete game (DELETE)
def delete_game_by_id(game_id: int, db: Session) -> Game:
    db_game = db.query(Game).filter(Game.id == game_id).first()
    
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(db_game)
    db.commit()
    
    return db_game

# filter by platform (GET)
def filter(platform: str, db: Session) -> List[Game]:
    db_game = db.query(Game).filter(Game.platform==platform).all()

    if not db_game:
            raise HTTPException(status_code=404, detail="No games under that platform")
    
    return db_game