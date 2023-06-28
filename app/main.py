#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Depends

from fastapi import FastAPI
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from datetime import datetime

from database import database, metadata, DATABASE_URL
from utils.helper import parse_name 

athlete_view = sqlalchemy.Table(
    "athlete_view",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(12), primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(128)),
    sqlalchemy.Column("last_name", sqlalchemy.String(128)),
    sqlalchemy.Column("gender", sqlalchemy.String(1)),
    sqlalchemy.Column("birth_year", sqlalchemy.Integer),
    sqlalchemy.Column("full_name", sqlalchemy.String(255)),
    sqlalchemy.Column("n_medals", sqlalchemy.Integer)
)

# Remplacer athlete view par la vraie table athlete

# La requête multitable aura lieu après

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

class newAthlete():
    id: str
    first_name: str
    last_name: str
    birth_year: int

class newAthleteIn():
    name: str = Field(...)

app.post("/createNewAthltete")
async def create_new_athlete(r: newAthleteIn = Depends(...)):
    query = newAthlete.insert().values(
        first_name = parse_name(r.name)["first"],
        last_name = parse_name(r.name)["last"]
    )
    record_id = await database.execute(query)
    query = athlete_view.select().where(athlete_view.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

app.get("/viewNewAthlete/{id}")
async def get_new_athlete(id: int):
    query = athlete_view.select().where(athlete_view.c.id == id)
    user = await database.fetch_one(query)
    return {**user}

# Faire un fetch all avec la vue 
