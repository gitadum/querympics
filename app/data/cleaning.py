#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from utils.helper import parse_name, closest_even
from utils.helper import give_person_id, give_games_id, get_numeric_id

# Lecture des données
os.chdir("./app/data/files/")
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
df = pd.concat([summer, winter])

# Nettoyage des variables de 'athlet'

# Nom
# On crée deux colonnes pour le prénom et le nom
_get_first_name = lambda s: parse_name(s)["first"].capitalize()
_get_last_name = lambda s: parse_name(s)["last"].upper()

df["FirstName"] = df.Name.apply(_get_first_name)
df["LastName"] = df.Name.apply(_get_last_name)

# On crée une variable 'ShortName',
# qui contient la forme courte du nom de l'athlète (prénom puis nom)
df["ShortName"] = df["FirstName"] + " " + df["LastName"]

# Age
# On s'assure que les ages non entiers
# ne correspondent qu'aux valeurs vides
df["intAge"] = df.Age.apply(lambda x: x.is_integer())
df.Age.isna().sum() == df[df["intAge"] == False].shape[0]
df["Age"] = df.Age.astype("Int64")
df.drop(columns=["intAge"], inplace=True)

# Année d'olympiade
df["Year"] = df.Year.astype("Int64")

# Pour calculer correctement l'année de naissance d'un participant aux JO
# On doit corriger l'année des derniers JO d'été de Tokyo
# Initialement prévus pour 2020, ils ont été reporté en 2021
# en raison de la pandémie de CoVid-19 survenue en 2020
df.loc[(df["City"] == "Tokyo") & (df["Year"] == 2020), "Year"] = 2021

# Calcul par participation de l'année de naissance approximative du participant
df["BirthYear"] = df["Year"] - df["Age"]

# On peut rétablir l'année des derniers JO de Tokyo à 2020
# Maintenant qu'une année de naissance approximative a été calculée
df.loc[(df["City"] == "Tokyo") & (df["Year"] == 2021), "Year"] = 2020

# Arrondi à l'année paire la plus proche
# Pour donner une période de 2 ans qui donne le droit aux erreurs
df["ApproxBirthYear"] = df["BirthYear"].apply(closest_even)

df["AthleteID"] = df.apply(lambda x: give_person_id(x.FirstName,
                                                    x.LastName,
                                                    x.Sex,
                                                    x.ApproxBirthYear),
                                                    axis=1)

df["AthleteID"] = df["AthleteID"].apply(get_numeric_id)

# Création d'un id par olympiade
assert (df["Games"].apply(lambda s: int(s.split(" ")[0])) == df["Year"]).all()
assert (df["Games"].apply(lambda s: s.split(" ")[1]) == df["Season"]).all()
df["GamesID"] = df.apply(lambda x: give_games_id(x.Year, x.Season), axis=1)

# # ATHLETES # #

# On commence par regrouper tous athlètes sous le même id d'athlète
# Nom de famille
athlet = (df.groupby("AthleteID")["LastName"].unique().to_frame())
assert athlet["LastName"].apply(len).all() == 1
athlet["LastName"] = athlet["LastName"].apply(lambda l: l[0])

# Prénom
athlet = athlet.join(df.groupby("AthleteID")["FirstName"].unique().to_frame())
assert athlet["FirstName"].apply(len).all() == 1
athlet["FirstName"] = athlet["FirstName"].apply(lambda l: l[0])

# Genre
athlet = athlet.join(df.groupby("AthleteID")["Sex"].unique().to_frame())
assert athlet["Sex"].apply(len).all() == 1
athlet["Sex"] = athlet["Sex"].apply(lambda l: l[0])
athlet["Sex"] = athlet["Sex"].astype("category")

# Age
athlet = athlet.join(df.groupby("AthleteID")["BirthYear"].mean().to_frame())
athlet["BirthYear"].fillna(0, inplace=True)
athlet["BirthYear"] = athlet["BirthYear"].apply(lambda y: round(y, 0))
athlet["BirthYear"] = athlet["BirthYear"].astype("Int64")
athlet["BirthYear"].replace(0, pd.NA, inplace=True)

# Dernier NOC
athlet = athlet.join(df
                     .sort_values(by="Year")
                     .groupby(["AthleteID"])["NOC"].last())

athlet = athlet.reset_index()

_person_cols = ["AthleteID", "FirstName", "LastName", "Sex", "BirthYear", "NOC"]
athlet = athlet[_person_cols]

_person_cols_renaming = {
    "AthleteID": "id",
    "FirstName": "first_name",
    "LastName": "last_name",
    "Sex": "gender",
    "BirthYear": "birth_year",
    "NOC": "lattest_noc"
}

athlet.rename(columns=_person_cols_renaming, inplace=True)
athlet.set_index("id", inplace=True)

# # GAMES # #

df.loc[df["Games"] == "1956 Summer", "City"] = \
    df.loc[df["Games"] == "1956 Summer", "City"].replace("Stockholm",
                                                         "Melbourne")

games = (
    df.groupby("Games")["GamesID"].unique().explode().to_frame().join(
    df.groupby("Games")["Year"].unique().explode().to_frame()).join(
    df.groupby("Games")["Season"].unique().explode().to_frame()).join(
    df.groupby("Games")["City"].unique().explode().to_frame())
    .reset_index())

assert df["Games"].nunique() == games.shape[0]

games["Season"] = games["Season"].astype("category")

_games_cols = ["GamesID", "Year", "Season", "City"]
games = games[_games_cols]

games.rename(columns={"GamesID": "ID"}, inplace=True)
# On passe le nom des colonnes en minuscule
games.columns = map(str.lower, games.columns)
games.set_index("id", inplace=True)

# # RESULTS # #

result = df.copy()
_result_cols = ["GamesID", "Sport", "Event", "AthleteID", "NOC", "Medal"]
result = result[_result_cols]

_medal_names = {"Gold": "G", "Silver": "S", "Bronze": "B"}
result["Medal"] = result["Medal"].replace(_medal_names)
result["Medal"] = result["Medal"].astype("category")

result.rename(columns={"AthleteID": "Athlete",
                       "GamesID": "Games"}, inplace=True)
result.columns = map(str.lower, result.columns)
result.rename_axis(index="id", inplace=True)

# # REGIONS # #

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
region.set_index("noc", inplace=True)

if __name__ == "__main__":
    # On crée le sous-dossier "/data/files/clean" s'il n'existe pas
    clean_dir = "clean" # chemin relatif depuis /data/files/
    if not os.path.exists(clean_dir):
        os.makedirs(clean_dir)
    # On enregistre les tables
    region.to_csv(f"{clean_dir}/regions.csv", sep=",", index=True)
    athlet.to_csv(f"{clean_dir}/athletes.csv", sep=",", index=True)
    games.to_csv(f"{clean_dir}/games.csv", sep=",", index=True)
    result.to_csv(f"{clean_dir}/results.csv", sep=",", index=True)
