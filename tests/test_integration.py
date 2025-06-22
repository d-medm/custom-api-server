import pytest 
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app
from app.database import get_db

# creating a separate database 
# so we dont perform operations on our main database
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    # drop then create tables so each time tests run 
    # tables refresh
    SQLModel.metadata.drop_all(engine) 
    SQLModel.metadata.create_all(engine) 
    """ fixture for creating a new database session for each test """
    with Session(engine) as session:
        yield session

# creating fake clients
@pytest.fixture(name="client")
def client_fixture(session):
    """Fixture for creating a new TestClient for each test."""
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# tests /games
def test_get_games(client):
    response = client.get("/games") #call /games endpoint
    assert response.status_code == 200 # assert it returns OK
    assert isinstance(response.json(), list) # assert what is returned is a str

# test POST /games
def test_create_game(client):
    # add a game
    response = client.post(
        "/games",
        json={"name": "FF7", "platform": "PS1"}
    )
    assert response.status_code == 200 
    assert response.json() == {
        "id":1,
        "name":"FF7",
        "platform":"PS1",
    }

# test GET /games/search
def test_search_game(client):
    q = "FF7"

    # first put something in the database
    add_game = client.post(
        "/games",
        json={"name": "FF7", "platform": "PS1"}
    )

    # then search
    response = client.get(
        f"/games/search?q={q}"
    )
    assert response.status_code == 200
    assert add_game.json()["name"] == q

# test GET /games/random
def test_generate_random_game(client):
    # first put something in the database
    client.post("/games", json={"name": "FF7", "platform": "PS1"})

    response = client.get("/games/random")
    print(response.json())

    assert response.status_code == 200 
    data = response.json()
    assert "name" in data and isinstance(data["name"], str)

# test GET /games/{game_id}
def test_get_game_id(client):
    # first put something in the database
    add_game = client.post(
        "/games",
        json={"name": "FF7", "platform": "PS1"}
    )

    # we expect id to be 1, since it is the 
    # first game added
    game_id = 1
    
    response = client.get(
        f"/games/{game_id}"
    )

    assert response.status_code == 200
    assert add_game.json()["id"] == game_id

# test PUT /games/{game_id}
def test_update_game(client):
    # first put something in the database
    client.post(
        "/games",
        json={"name": "FF7", "platform": "PS1"}
    )

    # we expect id to be 1, since it is the 
    # first game added, replace it with the 
    # new game
    game_id = 1
    
    response = client.put(
        f"/games/{game_id}",
        json={"name": "Resident Evil", "platform": "PS1"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "id":1,
        "name":"Resident Evil",
        "platform":"PS1",
    } 

# test DELETE /games/{game_id}
def test_delete_game(client):
    # first put something in the database
    client.post(
        "/games",
        json={"name": "FF7", "platform": "PS1"}
    )

    # we expect id to be 1, since it is the 
    # first game added, replace it with the 
    # new game
    game_id = 1
    
    response = client.delete(
        f"/games/{game_id}",
    )

    assert response.status_code == 200
    # we expect for the endpoint to return
    # the game it deleted
    assert response.json() == {
        "id":1,
        "name":"FF7",
        "platform":"PS1",
    } 

# test GET /games/platform/{platform}
def test_get_platform(client):
    # first put something in the database
    client.post(
        "/games",
        json={"name": "FF7", "platform": "PS1"}
    )

    # filter by PS1
    platform = 'PS1'
    
    response = client.get(
        f"/games/platform/{platform}",
    )

    assert response.status_code == 200
    # we expect for the endpoint to return the correct 
    # platform
    assert response.json()[0]["platform"] == platform
