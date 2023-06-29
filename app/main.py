#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import sqlalchemy

from database import database, metadata, DATABASE_URL, db_host

athlete_view = sqlalchemy.Table(
    "athlete_view",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(12), primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(128)),
    sqlalchemy.Column("last_name", sqlalchemy.String(128)),
    sqlalchemy.Column("gender", sqlalchemy.String(1)),
    sqlalchemy.Column("birth_year", sqlalchemy.Integer),
    sqlalchemy.Column("nocs", sqlalchemy.ARRAY(sqlalchemy.String(3))),
    sqlalchemy.Column("disciplines", sqlalchemy.ARRAY(sqlalchemy.String(32))),
    sqlalchemy.Column("n_medals", sqlalchemy.Integer)
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

class AthleteView(BaseModel):
    id: str
    first_name: str
    last_name: str
    gender: str
    birth_year: int
    nocs: list
    disciplines: list
    n_medals: int

@app.get("/")
async def greetings():
    return {"greetings": "Welcome to QUERYMPICS!"}

#class newAthleteIn():
#    first_name: str = Field(...)
#    last_name: str = Field(...)

#app.post("/createNewAthltete")
#async def create_new_athlete(r: newAthleteIn = Depends(...)):
#    query = AthleteView.insert().values(
#        first_name = parse_name(r.name)["first"],
#        last_name = parse_name(r.name)["last"]
#    )
#    record_id = await database.execute(query)
#    query = athlete_view.select().where(athlete_view.c.id == record_id)
#    row = await database.fetch_one(query)
#    return {**row}

app.get("/athlete/byname/{last_name}", response_model=AthleteView)
async def get_athlete_by_name(last_name: str):
    last_name = last_name.upper()
    query = athlete_view.select().where(athlete_view.c.last_name == last_name)
    user = await database.fetch_one(query)
    return {**user}

# Faire un fetch all avec la vue 
@app.get("/athlete/byname/multiple/{last_name}",
         response_model=List[AthleteView])
async def get_athletes_by_name(last_name: str):
    last_name = last_name.upper()
    query = athlete_view.select().where(athlete_view.c.last_name == last_name)
    all_get = await database.fetch_all(query)
    return all_get

if __name__ == "__main__":
    uvicorn.run(app, host=db_host, port=8000)
