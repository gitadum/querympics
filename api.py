#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException
from models import Result, Result_Pydantic, ResultIn_Pydantic
from models import Athlete, Athlete_Pydantic, AthleteIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel

from data.db import db_host, db_name, db_usr, db_pwd, db_port
from psycopg2 import connect

# Connexion à la base de données PostGre
connector = connect(host=db_host, dbname=db_name, user=db_usr, password=db_pwd,
                    port=db_port)
db_url = f"postgres://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}"

class Message(BaseModel):
    message: str = ""

app = FastAPI()

# ### MESSAGE D'ACCEUIL ### #

@app.get("/")
async def greetings():
    return {"greetings": "Welcome to QUERYMPICS!"}

# ### INTERACTION AVEC LA TABLE RESULT ### #

@app.get("/result/{id}",
         response_model=Result_Pydantic,
         responses={404: {"model": HTTPNotFoundError}})
async def get_a_result(id: str):
    return await Result_Pydantic.from_queryset_single(Result.get(id=id))

@app.post("/result/new/", response_model=Result_Pydantic)
async def write_result(result: Result_Pydantic):
    obj = await Result.create(**result.dict(exclude_unset=True))
    return await Result_Pydantic.from_tortoise_orm(obj)

@app.put("/result/{id}", response_model=Result_Pydantic,
         responses={404: {"model": HTTPNotFoundError}})
async def update_a_result(id: str, updated_result: ResultIn_Pydantic):
    await Result.filter(id=id).update(**updated_result.dict(exclude_unset=True))
    return await Result_Pydantic.from_queryset_single(Result.get(id=id))

@app.delete("/result/{id}", response_model=Message,
            responses={404: {"model": HTTPNotFoundError}})
async def delete_a_result(id: str):
    del_obj = await Result.filter(id=id).delete()
    if not del_obj:
        raise HTTPException(status_code=404, detail="Result not found.")
    return Message(message=f"Deleted {id}.")

# ### INTERACTION AVEC LA TABLE ATHLETE ### #

@app.get("/athlete/{id}",
         response_model=Athlete_Pydantic,
         responses={404: {"model": HTTPNotFoundError}})
async def get_an_athlete(id: str):
    return await Athlete_Pydantic.from_queryset_single(Athlete.get(id=id))

@app.post("/athlete/new/", response_model=Athlete_Pydantic)
async def write_athlete(athlete: Athlete_Pydantic):
    obj = await Athlete.create(**athlete.dict(exclude_unset=True))
    return await Athlete_Pydantic.from_tortoise_orm(obj)

@app.put("/athlete/{id}", response_model=Athlete_Pydantic,
         responses={404: {"model": HTTPNotFoundError}})
async def update_an_athlete(id: str, updated_athlete: AthleteIn_Pydantic):
    await Athlete.filter(id=id).update(**updated_athlete.dict(exclude_unset=True))
    return await Athlete_Pydantic.from_queryset_single(Athlete.get(id=id))

# Connexion à la base de données
register_tortoise(
    app,
    db_url=db_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
