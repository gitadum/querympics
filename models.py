#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional

password = "dummypassw0rd"

class ResultIn(BaseModel):
    id : str
    games: str
    sport: str
    event: Optional[str]
    athlete: str
    noc: str
    medal: Optional[str] = None
    password: str

class ResultOut(BaseModel):
    id : str
    games: str
    sport: str
    event: Optional[str]
    athlete: str
    noc: str
    medal: Optional[str] = None

class Athlete(BaseModel):
    first_name: str
    last_name: str
    gender: str
    birth_year: Optional[str]
    lattest_noc: Optional[str]
