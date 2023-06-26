#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from .models import Result, Result_Pydantic, ResultIn_Pydantic
from .models import Athlete, Athlete_Pydantic, AthleteIn_Pydantic
from .models import Message
from .database import DATABASE_URL, database, db_host

app = FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

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

@app.delete("/athlete/{id}", response_model=Message,
            responses={404: {"model": HTTPNotFoundError}})
async def delete_an_athlete(id: str):
    del_obj = await Athlete.filter(id=id).delete()
    if not del_obj:
        raise HTTPException(status_code=404, detail="Athlete not found.")
    return Message(message=f"Deleted {id}.")

# Connexion à la base de données
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == "__main__":
    uvicorn.run(app, host=db_host, port=8000)
