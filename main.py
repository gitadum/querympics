#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from utils import database

db_usr = "sqladum"
db_pwd = "dummypassw0rd"
db_name = "olympics"
db_host = "localhost"
db_port = 5432

engine_path = f"postgresql+psycopg2://{db_usr}:{db_pwd}@{db_host}/{db_name}"
engine = create_engine(engine_path)

data_dir = "./data/"
os.chdir(data_dir)

CREATE_ATHLETE = False
TRUNCATE_ATHLETE = False
FILL_ATHLETE = False
CREATE_GAMES = False
TRUNCATE_GAMES = False
FILL_GAMES = False
CREATE_REGION = False
TRUNCATE_REGION = False
FILL_REGION = False
CREATE_RESULT = True
TRUNCATE_RESULT = False
FILL_RESULT = True

# Connexion à la base de données PostGre
connector = psycopg2.connect(host=db_host, dbname=db_name,
                             user=db_usr, password=db_pwd,
                             port=db_port)
cursor = connector.cursor()

# Lancement des requêtes

# Création des tables
if CREATE_ATHLETE:
    create_athlete = "./base/athlete.create.sql"
    database.create_table("athlete", create_athlete, connector, cursor)

if CREATE_GAMES:
    create_games = "./base/games.create.sql"
    database.create_table("games", create_games, connector, cursor)

if CREATE_REGION:
    create_region = "./base/region.create.sql"
    database.create_table("region", create_region, connector, cursor)

if CREATE_RESULT:
    create_result = "./base/result.create.sql"
    database.create_table("result", create_result, connector, cursor)

# Troncature des tables
if TRUNCATE_ATHLETE:
    truncate_athlete = "./base/athlete.truncate.sql"
    database.truncate_table("athlete", truncate_athlete, connector, cursor)

if TRUNCATE_GAMES:
    truncate_games = "./base/games.truncate.sql"
    database.truncate_table("games", truncate_games, connector, cursor)

if TRUNCATE_REGION:
    truncate_region = "./base/region.truncate.sql"
    database.truncate_table("region", truncate_region, connector, cursor)

if TRUNCATE_RESULT:
    truncate_result = "./base/result.truncate.sql"
    database.truncate_table("result", truncate_result, connector, cursor)

# Remplissage des tables avec les CSV issus du nettoyage
if FILL_ATHLETE:
    athlete_file_path = "./files/clean/athletes.csv"
    database.fill_table_from_csv("athlete", athlete_file_path,
                                 connector, engine,
                                 verbose=True,
                                 fill_by_chuncks=True,
                                 n_chunk=10000)

if FILL_GAMES:
    games_file_path = "./files/clean/games.csv"
    database.fill_table_from_csv("games", games_file_path,
                                 connector, engine,
                                 verbose=True)

if FILL_REGION:
    region_file_path = "./files/clean/regions.csv"
    database.fill_table_from_csv("region", region_file_path,
                                 connector, engine,
                                 verbose=True)

if FILL_RESULT:
    result_file_path = "./files/clean/results.csv"
    database.fill_table_from_csv("result", result_file_path,
                                 connector, engine,
                                 verbose=True,
                                 fill_by_chuncks=True,
                                 n_chunk=10000)

cursor.close()
connector.close()

print("Query ended.")
