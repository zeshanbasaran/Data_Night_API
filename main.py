from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine
import sqlite3

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./dates.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


@app.get("/")
async def main_route():
    return {"message": "Welcome to our API!"}


class DateCreate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_name: str
    location: str


class Date(DateCreate):
    id: int


def create_connection():
    connection = sqlite3.connect("dates.db")
    return connection


def create_table():
    SQLModel.metadata.create_all(engine)

    # connection = create_connection()
    # cursor = connection.cursor()
    # try:
    #     cursor.execute(
    #         """
    #     CREATE TABLE IF NOT EXISTS dates (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     date_name TEXT NOT NULL,
    #     location TEXT NOT NULL
    #     )
    #     """
    #     )
    #     connection.commit()
    # except sqlite3.Error as e:
    #     print(f"Error creating table: {e}")
    # connection.close()


create_table()


def create_date(date: DateCreate):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO dates (date_name, location) VALUES (?, ?)",
            (date.date_name, date.location),
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        connection.close()


session = Session(engine)

def seed_db():
    data = [
        (1, "Skate", "Outside"),
        (2, "Cuddle", "Inside"),
        (3, "Get Starbucks", "Outside"),
        (4, ""),
    ]

    cur.executemany("INSERT INTO dates VALUES(?, ?, ?)", data)
    con.commit()
