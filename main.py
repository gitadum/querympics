#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

db_usr = "sqladum"
db_pwd = "dummypassw0rd"
db_name = "olympics"
db_host = "localhost"
db_port = 5432

engine_path = f"postgresql+psycopg2://{db_usr}:{db_pwd}@{db_host}/{db_name}"
engine = create_engine(engine_path)

data_dir = "./data/files/clean/"
os.chdir(data_dir)

CREATE_REGION = False
TRUNCATE_REGION = False
FILL_REGION = False
CREATE_ATHLETE = True
TRUNCATE_ATHLETE = True
FILL_ATHLETE = True

# Connexion à la base de données PostGre
connector = psycopg2.connect(host=db_host, dbname=db_name,
                             user=db_usr, password=db_pwd,
                             port=db_port)
cursor = connector.cursor()

# Lancement des requêtes
if CREATE_ATHLETE:
    print("Crating `athlete`...")
    with open("../../base/athlete.create.sql") as f:
        create_athlete_db = f.read()
    create_athlete_db = create_athlete_db.split(";")[0]
    #print(create_athlete_db)
    cursor.execute(create_athlete_db)
    connector.commit()
    print("Created `athlete`.")

if CREATE_REGION:
    print("Creating `region`...")
    with open("../../base/region.create.sql") as f:
        create_region_db = f.read()
    create_region_db = create_region_db.split(";")[0]
    #print(create_region_db)
    cursor.execute(create_region_db)
    connector.commit()
    print("Created `region`.")

if TRUNCATE_ATHLETE:
    print("Truncating `athlete`...")
    with open("../../base/athlete.truncate.sql") as f:
        truncate_athlete_db = f.read()
    truncate_athlete_db = truncate_athlete_db.split(";")[0]
    cursor.execute(truncate_athlete_db)
    connector.commit()
    print("Truncated `athlete`.")

if TRUNCATE_REGION:
    print("Truncating `region`...")
    with open("../../base/region.truncate.sql") as f:
        truncate_region_db = f.read()
    truncate_region_db = truncate_region_db.split(";")[0]
    cursor.execute(truncate_region_db)
    connector.commit()
    print("Truncated `region`.")

if FILL_REGION:
    # Remplissage de la table region
    print("Starting loading records into `athlete`...")
    region = pd.read_csv("regions.csv")
    region.to_sql("region", engine, if_exists="append", index=False)
    connector.commit()
    print("Done with loading records into `athlete`.")

if FILL_ATHLETE:
    # Remplissage de la table athlete par lot
    # la taille d'un lot est déterminé par "n_chunk"
    n_chunk = 10000
    i = 1
    n = 15
    print("Starting loading records into `athlete`...")
    for chunk in pd.read_csv("athletes.csv", chunksize=n_chunk):
        chunk.to_sql("athlete", engine, if_exists="append", index=False)
        print(f"loaded {n_chunk} records into athlete ({i}/{n}).")
        i += 1
    connector.commit()
    print("Done with loading records into `athlete`.")

cursor.close()
connector.close()

print("Query ended.")
