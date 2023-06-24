#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from typing import Optional

from olympics import ResultIn, ResultOut

app = FastAPI()

@app.post("/result/",
          response_model=ResultOut,
          response_model_exclude={"password"})
async def make_result(new_result: ResultIn):
    # db write completed
    assert new_result.password == "dummypassw0rd"
    return new_result

#get
@app.get("/")
async def greetings():
    return {"greetings": "Welcome to Querylimpics!"}

@app.get("/component/{component_id}") # path parameter
async def get_component(component_id: int):
    return {"component": component_id}

@app.get("/component/")
async def read_component(number: int, text: Optional[str]):
    return {"number": number, "text": text}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
