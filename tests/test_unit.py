import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.models import Game, GameCreate, GameResponse, GameUpdate

from app.logic import (
    create_game,
    get_all_games,
    search_games,
    get_random_games,
    get_game_by_id,
    update_game_by_id,
    delete_game_by_id,
    filter
)


def test_create_game():
    #create fake database
    mock_db = MagicMock()
    #mock finding duplicates
    mock_db.query().filter().first.return_value = None
    # mock (or fake input data) adding information to the 
    # database.
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # create game
    new_game = GameCreate(name="FF9", platform="PS1")

    # call create_game
    result = create_game(new_game, mock_db)

    # assert
    assert result.name == "FF9"
    assert result.platform == "PS1"

def test_get_all_games():
    mock_db = MagicMock()
    # add fake data
    fake_games = [
        Game(id=1, name="FF7", platform="PS1"),
        Game(id=2, name="FF8", platform="PS1")
    ]

    #mock querying all the data
    mock_db.query.return_value.all.return_value = fake_games
    result = get_all_games(mock_db)

    assert isinstance(result, list) # expecting a list
    assert len(result) == 2 # expecting two games
    assert result[0].name == "FF7"
    assert result[1].name == "FF8"

def test_search_games():
    mock_db = MagicMock()

     # add fake data
    fake_games = [
        Game(id=1, name="FF7", platform="PS1"),
        Game(id=2, name="FF8", platform="PS1")
    ]

    # mock searching for games
    mock_db.query.return_value.filter.return_value.all.return_value = fake_games
    q = 'f'
    result = search_games(q, mock_db)

    assert isinstance(result, list)
    assert len(result) == 2
    # assert that letter f is in all of the results
    assert all("f" in e.name.lower() and q.lower() in e.name.lower() 
               for e in result)
    
def test_get_random_games():
    mock_db = MagicMock()

    # add fake data
    fake_games = [
        Game(id=1, name="FF7", platform="PS1"),
        Game(id=2, name="FF8", platform="PS1")
    ]

    mock_db.query.return_value.all.return_value = fake_games

    result = get_random_games(mock_db)
    assert isinstance(result, Game)
    assert result in fake_games
    assert isinstance(result.name, str)

def test_get_game_by_id():
    mock_db = MagicMock()

    # add fake data
    fake_games = [
        Game(id=1, name="FF7", platform="PS1"),
        Game(id=2, name="FF8", platform="PS1")
    ]
    
    # get the first item
    mock_db.query.return_value.filter.return_value.first.return_value = fake_games[0]

    result = get_game_by_id(1, mock_db)
    assert isinstance(result, Game)
    assert result.name == "FF7"

def test_update_game_by_id():
    mock_db = MagicMock()

    # add fake data
    fake_games = [
        Game(id=1, name="FF7", platform="PS1"),
    ]

    mock_db.query.return_value.filter.return_value.first.return_value = fake_games[0]

    update = GameUpdate(id=1, name="FF15", platform="PS4")
    

    result = update_game_by_id(1, update, mock_db)
    assert isinstance(result, Game)
    assert result.name == "FF15"

def test_delete_game_by_id():
    mock_db = MagicMock()

    # add fake data
    fake_games = [
        Game(id=1, name="FF7", platform="PS1"),
    ]

    mock_db.query.return_value.filter.return_value.first.return_value = fake_games[0]

    result = delete_game_by_id(1, mock_db)
    assert isinstance(result, Game)
    assert result.id == 1
    assert result.name == "FF7"

def test_filter():
    mock_db = MagicMock()

    # add fake data
    fake_games = [
        Game(id=1, name="FF7", platform="PS1"),
        Game(id=2, name="FF15", platform="PS5"),
        Game(id=3, name="Kingdom Hearts", platform="PS2"),
    ]

    mock_db.query.return_value.filter.return_value.all.return_value = fake_games
    
    platform = "PS"
    result = filter(platform, mock_db)

    assert isinstance(result, list)
    assert all(platform.lower() in e.platform.lower() 
               for e in result)