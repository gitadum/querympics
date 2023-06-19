#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

# Lecture des données
os.chdir("./data/files/")
summer = pd.read_csv("Athletes_summer_games.csv", index_col=0)
winter = pd.read_csv("Athletes_winter_games.csv", index_col=0)
region = pd.read_csv("regions.csv", index_col=0)

# # ATHLETES # #

# On réinitialise la colonne d'index (qui n'est pas unique)
summer = summer.reset_index(drop=True)
winter = winter.reset_index(drop=True)

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

if __name__ == "__main__":
    # On crée le sous-dossier "/data/files/clean" s'il n'existe pas
    clean_dir = "clean" # chemin relatif depuis /data/files/
    if not os.path.exists(clean_dir):
        os.makedirs(clean_dir)
    # On enregistre la table
    region.to_csv(f"{clean_dir}/regions.csv", sep=",", index=None)
