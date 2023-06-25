#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import databases
import sqlalchemy

from datetime import datetime

# # BASE DE DONNÉES  # #

db_usr = "sqladum"
db_pwd = "dummypassw0rd"
db_name = "olympics"
db_host = "localhost"
db_port = 5432

DATABASE_URL = f"postgres://{db_usr}:{db_pwd}@{db_host}:{db_port}/test"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

register = sqlalchemy.table(
    "register",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255)),
    sqlalchemy.Column("date_created", sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)


# # API # #

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()
