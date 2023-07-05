#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, Extra, Field

class Message(BaseModel):
    message: str = ""


class Result(BaseModel):

    id: str
    games: str
    sport: str
    event: str
    athlete: str
    noc: str
    medal: str

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid


class ResultIn(BaseModel):

    season: Optional[str]
    year: Optional[int]
    sport: Optional[str]
    event: Optional[str]
    athlete: Optional[str]
    noc: Optional[str]
    medal: Optional[str]

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid


class Athlete(BaseModel):

    id: str = Field(..., max_length=12) # Clé primaire
    first_name: str = Field(None, max_length=128)
    last_name: str = Field(None, max_length=128)
    gender: str = Field(None, max_length=1)
    birth_year: int = Field(None)
    lattest_noc: str = Field(None, max_length=3)


class AthleteIn(BaseModel):

    id: str = Field(..., max_length=12) # Clé primaire
    first_name: str = Field(None, max_length=128)
    last_name: str = Field(None, max_length=128)
    gender: str = Field(None, max_length=1)
    birth_year: int = Field(None)
    lattest_noc: str = Field(None, max_length=3)


class AthleteView(BaseModel):
    id: str
    first_name: str
    last_name: str
    gender: Optional[str]
    birth_year: Optional[str]
    nocs: List[str]
    disciplines: List[str]
    n_medals: int
