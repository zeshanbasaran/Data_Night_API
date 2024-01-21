from fastapi import FastAPI  
from pydantic import BaseModel
import sqlite3

app = FastAPI()   
@app.get("/") 
async def main_route():     
    return {"message": "Welcome to our API!"}

class DateCreate(BaseModel):
    date_name: str
    location: str

class Date(DateCreate):
    id: int

def create_connection():
    connection = sqlite3.connect("dates.db")
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_name TEXT NOT NULL,
        location TEXT NOT NULL
        )
        """)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    connection.close()

create_table() # Call this function to create the table

def create_date(date: DateCreate):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO dates (date_name, location) VALUES (?, ?)", (date.date_name, date.location))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        connection.close()

d1 = DateCreate("Eating Out", "Bed")