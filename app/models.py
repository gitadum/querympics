#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Optional, List
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Extra
from utils.helper import give_games_id

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

    def gen_games_id(self):
        self.games = give_games_id(self.year, self.season)

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid

class Athlete(models.Model):

    id = fields.CharField(pk=True, max_length=12)
    first_name = fields.CharField(max_length=128, null=True)
    last_name = fields.CharField(max_length=128, null=True)
    gender = fields.CharField(max_length=1, null=True)
    birth_year = fields.SmallIntField(null=True)
    lattest_noc = fields.CharField(max_length=3, null=True)

class AthleteIn(models.Model):

    id = fields.CharField(pk=True, max_length=12)
    first_name = fields.CharField(max_length=128, null=True)
    last_name = fields.CharField(max_length=128, null=True)
    gender = fields.CharField(max_length=1, null=True)
    birth_year = fields.SmallIntField(null=True)
    lattest_noc = fields.CharField(max_length=3, null=True)

Athlete_Pydantic = pydantic_model_creator(Athlete, name="Athlete")
AthleteIn_Pydantic = pydantic_model_creator(Athlete, name="AthleteIn",
                                            exclude_readonly=True)

class AthleteView(BaseModel):
    id: str
    first_name: str
    last_name: str
    gender: Optional[str]
    birth_year: Optional[str]
    nocs: List[str]
    disciplines: List[str]
    n_medals: int
