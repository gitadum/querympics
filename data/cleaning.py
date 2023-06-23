#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from utils.helper import parse_name, closest_even
from utils.helper import give_person_id, get_numeric_id

# Lecture des données
os.chdir("./data/files/")
summer = pd.read_csv("Athletes_summer_games.csv", index_col=0)
winter = pd.read_csv("Athletes_winter_games.csv", index_col=0)
region = pd.read_csv("regions.csv", index_col=0)

# # ATHLETES # #

# On réinitialise la colonne d'index (qui n'est pas unique)
summer = summer.reset_index(drop=True)
winter = winter.reset_index(drop=True)

# Reconstruction de l'index
_newindex = lambda idx, letter: letter + str(idx + 1).zfill(6)
summer["new_index"] = summer.reset_index()["index"].apply(_newindex, letter="S")
winter["new_index"] = winter.reset_index()["index"].apply(_newindex, letter="W")
summer = summer.set_index("new_index").rename_axis(index="index")
winter = winter.set_index("new_index").rename_axis(index="index")

# On s'assure que les colonnes sont les mêmes
# pour les JO d'été que pour les JO d'hiver
assert list(summer.columns) == list(winter.columns)
assert (summer.dtypes == winter.dtypes).all()

# Concaténation des JO d'été et d'hiver
athlet = pd.concat([summer, winter])

# Nettoyage des variables de 'athlet'

# Nom
# On crée deux colonnes pour le prénom et le nom
_get_first_name = lambda s: parse_name(s)["first"].capitalize()
_get_last_name = lambda s: parse_name(s)["last"].upper()

athlet["FirstName"] = athlet.Name.apply(_get_first_name)
athlet["LastName"] = athlet.Name.apply(_get_last_name)

# On crée une variable 'ShortName',
# qui contient la forme courte du nom de l'athlète (prénom puis nom)
athlet["ShortName"] = athlet["FirstName"] + " " + athlet["LastName"]

# Age
# On s'assure que les ages non entiers
# ne correspondent qu'aux valeurs vides
athlet["intAge"] = athlet.Age.apply(lambda x: x.is_integer())
athlet.Age.isna().sum() == athlet[athlet["intAge"] == False].shape[0]
athlet["Age"] = athlet.Age.astype("Int64")
athlet.drop(columns=["intAge"], inplace=True)

# Année d'olympiade
athlet["Year"] = athlet.Year.astype("Int64")

# Calcul de l'année de naissance
athlet["BirthYear"] = athlet["Year"] - athlet["Age"]

# Arrondi à l'année paire la plus proche
# Pour donner une période de 2 ans qui donne le droit aux erreurs
athlet["YOB"] = athlet["BirthYear"].apply(closest_even)

athlet["AthleteID"] = athlet.apply(lambda x: give_person_id(x.FirstName,
                                                            x.LastName,
                                                            x.Sex,
                                                            x.YOB), axis=1)

athlet["AthleteID"] = athlet["AthleteID"].apply(get_numeric_id)

# person
person = athlet.groupby("AthleteID").Games.nunique().reset_index()
n_person = person.shape[0]
person['g'] = person.groupby('AthleteID').cumcount()
athlet.sort_values(by="Year", ascending=False, inplace=True)
athlet['g'] = athlet.groupby('AthleteID').cumcount()
person_cols = ["AthleteID", "FirstName", "LastName", "Sex", "BirthYear", "NOC"]

person = person.merge(athlet[person_cols + ["g"]], on="AthleteID", how="left")
person = person[person["g_y"] == 0]

assert person.shape[0] == n_person

person = person[person_cols]

_person_cols_renaming = {
    "AthleteID": "id",
    "FirstName": "first_name",
    "LastName": "last_name",
    "Sex": "gender",
    "BirthYear": "birth_year",
    "NOC": "lattest_noc"
}

person.rename(columns=_person_cols_renaming, inplace=True)

athlet.drop(columns=["g"], inplace=True)

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
    # On enregistre les tables
    region.to_csv(f"{clean_dir}/regions.csv", sep=",", index=None)
    person.to_csv(f"{clean_dir}/athletes.csv", sep=",", index=None)
