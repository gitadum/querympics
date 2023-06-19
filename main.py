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

region = pd.read_csv("regions.csv")

# Connexion à la base de données PostGre
connector = psycopg2.connect(host=db_host, dbname=db_name,
                             user=db_usr, password=db_pwd,
                             port=db_port)
cursor = connector.cursor()

# Ici on lancera les requêtes qui iront bien
cursor.execute("""
CREATE TABLE IF NOT EXISTS athlete (

id VARCHAR(7) PRIMARY KEY,
name VARCHAR(128),
sex CHAR,
age INT,
team VARCHAR(64),
noc VARCHAR(3),
games VARCHAR(11),
year INT,
season VARCHAR(6),
city VARCHAR(32),
event VARCHAR(128),
medal VARCHAR(6)

);
""")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS region (
    noc CHAR(3) PRIMARY KEY,
    region VARCHAR(32),
    notes VARCHAR(32)
    );
    """
)

# Remplissage de la table region
region.to_sql("region", engine, if_exists="append", index=False)

connector.commit()
cursor.close()
connector.close()

print("Query ended.")
