#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI

app = FastAPI()

#get
@app.get("/")
async def greetings():
    return {"greetings": "Welcome to Querylimpics!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
