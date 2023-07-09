#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, Extra, Field

class Message(BaseModel):
    message: str = ""


class Result(BaseModel):

    id: str = Field(..., max_length=7) # Clé primaire
    games: str = Field(None, max_length=5)
    sport: str = Field(None, max_length=32)
    event: str = Field(None, max_length=128)
    athlete: str = Field(None, max_length=12)
    noc: str = Field(None, max_length=3)
    medal: Optional[str] = Field(None, max_length=1)

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid


class ResultIn(BaseModel):

    season: Optional[str] = Field(None, max_length=6)
    year: Optional[int] = Field(None)
    sport: Optional[str] = Field(None, max_length=32)
    event: Optional[str] = Field(None, max_length=128)
    athlete: Optional[str] = Field(None, max_length=12)
    noc: Optional[str] = Field(None, max_length=3)
    medal: Optional[str] = Field(None, max_length=1)

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid


class Athlete(BaseModel):

    id: str = Field(..., max_length=12) # Clé primaire
    first_name: str = Field(None, max_length=128)
    last_name: str = Field(None, max_length=128)
    gender: str = Field(None, max_length=1)
    birth_year: Optional[int] = Field(None)
    lattest_noc: str = Field(None, max_length=3)

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid


class AthleteIn(BaseModel):

    first_name: str = Field(None, max_length=128)
    last_name: str = Field(None, max_length=128)
    gender: str = Field(None, max_length=1)
    birth_year: Optional[int] = Field(None)
    lattest_noc: Optional[str] = Field(None, max_length=3)

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid


class AthleteView(BaseModel):
    id: str
    first_name: str
    last_name: str
    gender: str
    birth_year: Optional[str]
    nocs: List[Optional[str]]
    disciplines: List[Optional[str]]
    n_medals: Optional[int]


class RegionView(BaseModel):
    region: str
    sport: str
    season: str
    year: int
    n_medals: Optional[int]
