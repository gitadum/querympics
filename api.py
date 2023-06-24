#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI

app = FastAPI()

#get
@app.get("/")
async def greetings():
    return {"greetings": "Welcome to Querylimpics!"}