#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import Extra

class Result(models.Model):

    id = fields.CharField(pk=True, max_length=7)
    games = fields.CharField(max_length=5, null=True)
    sport = fields.CharField(max_length=32, null=True)
    event = fields.CharField(max_length=128, null=True)
    athlete = fields.CharField(max_length=12, null=True)
    noc = fields.CharField(max_length=3, null=True)
    medal = fields.CharField(max_length=1, null=True)

    class PydanticMeta:
        pass

    class Config:
        extra = Extra.forbid

Result_Pydantic = pydantic_model_creator(Result, name="Result")
ResultIn_Pydantic = pydantic_model_creator(Result, name="ResultIn",
                                           exclude_readonly=True)
