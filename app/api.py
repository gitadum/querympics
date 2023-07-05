#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from typing import List

try:
    from .models import Result, ResultIn
    from .models import Athlete, AthleteIn
    from .models import AthleteView
    from .models import Message
    from .database import DATABASE_URL, database, db_host
    from .database import result, athlete, athlete_view
    from .utils.helper import give_games_id
except ImportError:
    from models import Result, ResultIn
    from models import Athlete, AthleteIn
    from models import AthleteView
    from models import Message
    from database import DATABASE_URL, database, db_host
    from database import result, athlete, athlete_view
    from utils.helper import give_games_id

app = FastAPI(title="Querympics", version="0.2.0-rc")

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
    season = "S" if new_result["season"] == "Summer" else "W"
    count_query = f"SELECT COUNT(id) FROM result WHERE games LIKE '{season}%'"
    n_results = await database.execute(count_query)
    new_result_id = "".join([season, str(n_results).zfill(6)])
    new_result_games = give_games_id(new_result["year"],
                                     new_result["season"])

    query = result.insert().values(
        id = new_result_id,
        games = new_result_games,
        sport = new_result["sport"],
        event = new_result["event"],
        athlete = new_result["athlete"],
        noc = new_result["noc"],
        medal = new_result["medal"]
    )

    await database.execute(query)
    return await database.fetch_one(result.select()
                                          .where(result.c.id == new_result_id))

@app.put("/result/{id}", response_model=Result,
         responses={404: {"model": HTTPNotFoundError}})
async def update_a_result(id: str, update_input: ResultIn = Depends()):
    stored_item_query = result.select().where(result.c.id == id)
    stored_item = await database.fetch_one(stored_item_query)
    update_result = update_input.dict(exclude_unset=True)
    try:
        if (update_result["season"] is not None
            and update_result["year"] is not None):
            update_result["games"] = give_games_id(update_result["year"],
                                                   update_result["season"])
    except KeyError:
        pass
    del update_result["season"]
    del update_result["year"]
    # On remplace les champs non renseignés
    # par les champs déjà remplis dans la base de données
    for key in update_result.keys():
        if update_result[key] is None:
            update_result[key] = stored_item[key]
    query = result.update().where(result.c.id==id).values(**update_result)
    await database.execute(query)
    get_updated_result = result.select().where(result.c.id == id)
    return await database.fetch_one(get_updated_result)

@app.delete("/result/{id}", response_model=Message,
            responses={404: {"model": HTTPNotFoundError}})
async def delete_a_result(id: str):
    query = result.delete().where(result.c.id == id)
    await database.execute(query)
    return Message(message=f"Deleted {id}.")

# # ### INTERACTION AVEC LA TABLE ATHLETE ### #

@app.get("/athlete/{id}",
         response_model=Athlete,
         responses={404: {"model": HTTPNotFoundError}})
async def get_an_athlete(id: str):
    query = athlete.select().where(athlete.c.id == id)
    get_one = await database.fetch_one(query)
    return get_one

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
