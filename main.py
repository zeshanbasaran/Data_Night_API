from fastapi import FastAPI, Response
from typing import Optional, List
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
import sqlite3


SQLALCHEMY_DATABASE_URL = "sqlite:///./dates.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

class Date(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_name: str
    location: str

# End-points
app = FastAPI()

@app.get("/")
async def main_route():
    return {"message": "Welcome to our API!"}


@app.get("/all-dates", response_model=List[Date])
async def dates_route():
    with Session(engine) as session:
        return session.exec(select(Date)).all()

def create_table():
    SQLModel.metadata.create_all(engine)

def seed_db():
    data = [
        Date(date_name="Skate", location="Outside"),
        Date(date_name="Cuddle", location="Inside"),
        Date(date_name="Get Starbucks", location="Outside"),
    ]

    with Session(engine) as session:
        for d in data:
            session.add(d)

        session.commit()

if __name__ == "__main__":
    create_table()
    seed_db()