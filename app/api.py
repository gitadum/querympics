#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from typing import List

try:
    from .models import Result, ResultIn
    from .models import Athlete, AthleteIn
    from .models import AthleteView
    from .models import Message
    from .database import database, db_host
    from .database import result, athlete, athlete_view
    from .utils.helper import give_games_id, give_person_id
    from .utils.helper import closest_even, get_numeric_id
except ImportError:
    from models import Result, ResultIn
    from models import Athlete, AthleteIn
    from models import AthleteView
    from models import Message
    from database import database, db_host
    from database import result, athlete, athlete_view
    from utils.helper import give_games_id, give_person_id
    from utils.helper import closest_even, get_numeric_id

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
         )
async def get_a_result(id: str):
    query = result.select().where(result.c.id == id)
    get_one = await database.fetch_one(query)
    try:
        assert get_one is not None
    except:
        raise HTTPException(404, f"result {id} not found.")
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

@app.put("/result/{id}",
         response_model=Result,
         )
async def update_a_result(id: str, update_input: ResultIn = Depends()):
    stored_item_query = result.select().where(result.c.id == id)
    stored_item = await database.fetch_one(stored_item_query)

    # On vérifie que l'élément existe dans cette table
    try:
        assert stored_item is not None
    except:
        raise HTTPException(404, f"result {id} not found.")

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

@app.delete("/result/{id}",
            response_model=Message,
            )
async def delete_a_result(id: str):
    deletable_item_query = result.select().where(result.c.id == id)
    deletable_item = await database.fetch_one(deletable_item_query)
    try:
        assert deletable_item is not None
    except:
        raise HTTPException(404, f"result {id} not found.")
    query = result.delete().where(result.c.id == id)
    await database.execute(query)
    return Message(message=f"Deleted {id}.")

# # ### INTERACTION AVEC LA TABLE ATHLETE ### #

@app.get("/athlete/{id}",
         response_model=Athlete,
         )
async def get_an_athlete(id: str):
    query = athlete.select().where(athlete.c.id == id)
    get_one = await database.fetch_one(query)
    try:
        assert get_one is not None
    except:
        raise HTTPException(404, f"athlete {id} not found.")
    return get_one

@app.post("/athlete/new",
          response_model=Athlete
          )
async def write_an_athlete(new: AthleteIn = Depends()):
    new = new.dict()
    # Génération de l'ID Athlète
    # à partir des infos en entrée
    approx_birth_year = closest_even(new["birth_year"])
    new_id = give_person_id(new["first_name"],
                            new["last_name"],
                            new["gender"],
                            approx_birth_year)
    # Transformation de l'ID Athlète en hash numérique
    new_id = get_numeric_id(new_id)

    # Formatage des noms et prénoms de l'athlète
    new_first_name = new["first_name"].capitalize()
    new_last_name = new["last_name"].upper()

    query = athlete.insert().values(
        id = new_id,
        first_name = new_first_name,
        last_name = new_last_name,
        gender = new["gender"],
        birth_year = new["birth_year"],
        lattest_noc = new["lattest_noc"]
    )
    await database.execute(query)

    new_item_query = athlete.select().where(athlete.c.id == new_id)
    new_item = await database.fetch_one(new_item_query)
    return new_item

@app.put("/athlete/{id}",
         response_model=Athlete,
         )
async def update_an_athlete(id: str, update_input: AthleteIn = Depends()):
    stored_item_query = athlete.select().where(athlete.c.id == id)
    stored_item = await database.fetch_one(stored_item_query)

    try:
        assert stored_item is not None
    except:
        raise HTTPException(404, f"athlete {id} not found.")

    update = update_input.dict(exclude_unset=True)

    # On remplace les champs non renseignés
    # par les champs déjà remplis dans la base de données
    for key in update.keys():
        if update[key] is None:
            update[key] = stored_item[key]
    query = athlete.update().where(athlete.c.id==id).values(**update)
    await database.execute(query)
    updated_item_query = athlete.select().where(athlete.c.id == id)
    updated_item = await database.fetch_one(updated_item_query)
    return updated_item

@app.delete("/athlete/{id}",
            response_model=Message,
            )
async def delete_an_athlete(id: str):
    deletable_item_query = athlete.select().where(athlete.c.id == id)
    deletable_item = await database.fetch_one(deletable_item_query)
    try:
        assert deletable_item is not None
    except:
        raise HTTPException(404, f"athlete {id} not found.")
    
    query = athlete.delete().where(athlete.c.id == id)
    await database.execute(query)
    return Message(message=f"Deleted {id}.")

# Faire un fetch all avec la vue 
@app.get("/search/athlete",
         response_model=List[AthleteView])
async def get_athletes_by_name(last_name: str):
    last_name = last_name.upper()
    query = (athlete_view
             .select()
             .where(athlete_view.c.last_name.like(f"%{last_name}%")))
    all_get = await database.fetch_all(query)
    try:
        assert all_get != []
    except:
        raise HTTPException(404, f"No athlete found for the name '{last_name}'")
    return all_get

if __name__ == "__main__":
    uvicorn.run(app, host=db_host, port=8000)
