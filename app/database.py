import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel, create_engine

load_dotenv()

# database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create tables
SQLModel.metadata.create_all(bind=engine)

# dependency to get db session
def get_db():
    with Session(engine) as session:
        yield session