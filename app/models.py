from sqlmodel import SQLModel, Field

# database model
class Game(SQLModel, table=True):
    __tablename__ = "games"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    platform: str

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