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


result1 = ResultIn(
    id="S000001",
    games="S1992",
    sport="Basketball",
    event="Basketball Men's Basketball",
    athlete="995417935682",
    noc="CHN",
    password=password
)

result2 = ResultIn(
    id="S000004",
    games="S1900",
    sport="Tug-Of-War",
    event="Tug-Of-War Men's Tug-Of-War",
    athlete="341882753977",
    noc="DEN",
    medal="G",
    password=password
)