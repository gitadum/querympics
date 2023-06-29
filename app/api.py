#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from typing import List

try:
    from .models import Result, ResultIn
    from .models import Athlete, Athlete_Pydantic, AthleteIn_Pydantic
    from .models import AthleteView
    from .models import Message
    from .database import DATABASE_URL, database, db_host
    from .database import result, athlete_view
except ImportError:
    from models import Result, ResultIn
    from models import Athlete, Athlete_Pydantic, AthleteIn_Pydantic
    from models import AthleteView
    from models import Message
    from database import DATABASE_URL, database, db_host
    from database import result, athlete_view

app = FastAPI(title="Querympics", version="0.2.0-alpha")

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

# ### MESSAGE D'ACCUEIL ### #

@app.get("/")
async def greetings():
    return {"greetings": "Welcome to QUERYMPICS!"}

# ### INTERACTION AVEC LA TABLE RESULT ### #

@app.get("/result/{id}",
         response_model=Result,
         responses={404: {"model": HTTPNotFoundError}})
async def get_a_result(id: str):
    query = result.select().where(result.c.id == id)
    get_one = await database.fetch_one(query)
    return get_one

@app.post("/result/new", response_model=Result)
async def write_result(new_result: ResultIn = Depends()):
    new_result = new_result.dict()
    #new_result_out = Result()
    n_results = database.execute("SELECT COUNT(id) FROM results")
    new_result_id = "S" if new_result["season"] == "Summer" else "W"
    new_result_id = "".join([new_result_id, str(n_results)])
    #new_result_out.id = new_result_id
    query = result.insert().values(
        id = new_result_id,
        games = new_result["games"],
        sport = new_result["sport"],
        event = new_result["event"],
        athlete = new_result["athlete"],
        noc = new_result["noc"],
        medal = new_result["medal"]

    )
    #await database.execute(query)
    #return {"season": new_result_id}
    return {**new_result}

# @app.put("/result/{id}", response_class=Result,
#          responses={404: {"model": HTTPNotFoundError}})
# async def update_a_result(id: str, updated_result: ResultIn):
#     await Result.filter(id=id).update(**updated_result.dict(exclude_unset=True))
#     return await Result.from_queryset_single(Result.get(id=id))

# @app.delete("/result/{id}", response_model=Message,
#             responses={404: {"model": HTTPNotFoundError}})
# async def delete_a_result(id: str):
#     del_obj = await Result.filter(id=id).delete()
#     if not del_obj:
#         raise HTTPException(status_code=404, detail="Result not found.")
#     return Message(message=f"Deleted {id}.")

# # ### INTERACTION AVEC LA TABLE ATHLETE ### #

# @app.get("/athlete/{id}",
#          response_model=Athlete_Pydantic,
#          responses={404: {"model": HTTPNotFoundError}})
# async def get_an_athlete(id: str):
#     return await Athlete_Pydantic.from_queryset_single(Athlete.get(id=id))

# @app.post("/athlete/new/", response_model=Athlete_Pydantic)
# async def write_athlete(athlete: Athlete_Pydantic):
#     obj = await Athlete.create(**athlete.dict(exclude_unset=True))
#     return await Athlete_Pydantic.from_tortoise_orm(obj)

# @app.put("/athlete/{id}", response_model=Athlete_Pydantic,
#          responses={404: {"model": HTTPNotFoundError}})
# async def update_an_athlete(id: str, updated_athlete: AthleteIn_Pydantic):
#     await Athlete.filter(id=id).update(**updated_athlete.dict(exclude_unset=True))
#     return await Athlete_Pydantic.from_queryset_single(Athlete.get(id=id))

# @app.delete("/athlete/{id}", response_model=Message,
#             responses={404: {"model": HTTPNotFoundError}})
# async def delete_an_athlete(id: str):
#     del_obj = await Athlete.filter(id=id).delete()
#     if not del_obj:
#         raise HTTPException(status_code=404, detail="Athlete not found.")
#     return Message(message=f"Deleted {id}.")

# Faire un fetch all avec la vue 
@app.get("/athlete/byname",
         response_model=List[AthleteView])
async def get_athletes_by_name(last_name: str):
    last_name = last_name.upper()
    query = athlete_view.select().where(athlete_view.c.last_name == last_name)
    all_get = await database.fetch_all(query)
    return all_get

# Connexion à la base de données
# register_tortoise(
#     app,
#     db_url=DATABASE_URL,
#     modules={"models": ["models"]},
#     generate_schemas=True,
#     add_exception_handlers=True
# )

if __name__ == "__main__":
    uvicorn.run(app, host=db_host, port=8000)
