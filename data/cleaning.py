#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

# Lecture des données
os.chdir("./data/")
summer = pd.read_csv("Athletes_summer_games.csv")
winter = pd.read_csv("Athletes_winter_games.csv")
region = pd.read_csv("regions.csv", index_col=0)
