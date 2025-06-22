import pytest 
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.routes
from app.models import Game, GameCreate, GameResponse, GameUpdate

def test_add_game(client):
    data = {
        "name":"testgame",
        "platform":"testplatform"
    }

    reponse = client.post("/games")