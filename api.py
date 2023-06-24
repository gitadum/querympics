#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

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
