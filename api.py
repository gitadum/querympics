#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, HTTPException, Form
from typing import List, Optional

from olympics import ResultIn, ResultOut
from olympics import result1, result2

app = FastAPI(title="Querympics")

# GET #

# Salutations
@app.get("/")
async def greetings():
    return {"greetings": "Welcome to Querympics!"}

# Composants
@app.get("/component/{component_id}") # path parameter
async def get_component(component_id: int):
    return {"component": component_id}

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

@app.get("/component/")
async def read_component(number: int, text: Optional[str]):
    return {"number": number, "text": text}

# Results

## Récupérer toutes les lignes
all_results = [result1, result2]
@app.get("/result/", response_model=List[ResultOut])
async def get_all_results():
    return all_results

##  Results: Récupérer une ligne
@app.get("/result/{id}", response_model=ResultOut)
async def get_result(id: str):
    try:
        return all_results[int(id)]
    except KeyError:
        raise HTTPException(status_code=404, detail="Result ID not found.")

# POSTS # 

# Result
@app.post("/result/write/",
          response_model=ResultOut,
          response_model_exclude={"password"})
async def write_result(new_result: ResultIn):
    try:
        assert new_result.password == "dummypassw0rd"
    except AssertionError:
        raise HTTPException(status_code=403, detail="Wrong password.")
    try:
        all_results.append(new_result)
    except:
        raise HTTPException(status_code=400, detail="Unknown error.")
    return new_result

# PUT #

# Result
@app.put("/result/{id}")
async def update_result(id: int, updated_result: ResultOut):
    try:
        all_results[id] = updated_result
        return all_results[id]
    except:
        raise HTTPException(status_code=404, detail="Result ID not found.")

# # DELETE # #

@app.delete("/result/{id}")
async def delete_result(id: int):
    try:
        obj = all_results[id]
        all_results.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Result ID not found.")

# MAIN #

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
