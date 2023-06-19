#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

# Lecture des données
os.chdir("./data/files/")
summer = pd.read_csv("Athletes_summer_games.csv")
winter = pd.read_csv("Athletes_winter_games.csv")
region = pd.read_csv("regions.csv", index_col=0)

# # REGIONS # #

# Lecture de la table
region = pd.read_csv("regions.csv", index_col=0)

# On vérifie que les valeurs de la colonne "NOC" sont uniques
# Ça sera la clé primaire de la table
assert region.shape[0] == region.NOC.nunique()

# Remplissage des libellés de région vides
# à partir de la colonne "notes"
region.loc[region["NOC"] == "ROT", "region"] = "Refugee"
region.loc[region["NOC"] == "TUV", "region"] = "Tuvalu"
region.loc[region["NOC"] == "UNK", "region"] = "Unknown"

# On passe le nom des colonnes en minuscule
region.columns = map(str.lower, region.columns)

# On enregistre la table
region.to_csv("regions.csv", sep=",", index=None)
