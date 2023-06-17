#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2

# Connexion à la base de données PostGre
connector = psycopg2.connect(host="localhost",
                             dbname="olympics",
                             user="sqladum",
                             password="dummypassw0rd",
                             port=5432)
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

connector.commit()
cursor.close()
connector.close()

print("Query ended.")
