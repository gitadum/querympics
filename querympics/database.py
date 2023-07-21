#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import databases
import sqlalchemy

# # BASE DE DONNÉES  # #

db_usr = "sqladum"
db_pwd = "dummypassw0rd"
db_name = "olympics"
db_host = "172.22.0.2"
db_port = 5432

DATABASE_URL = f"postgresql://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

# Result
result = sqlalchemy.Table(
    "result",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(7), primary_key=True),
    sqlalchemy.Column("games", sqlalchemy.String(5)),
    sqlalchemy.Column("sport", sqlalchemy.String(32)),
    sqlalchemy.Column("event", sqlalchemy.String(128)),
    sqlalchemy.Column("athlete", sqlalchemy.String(12)),
    sqlalchemy.Column("noc", sqlalchemy.String(3)),
    sqlalchemy.Column("medal", sqlalchemy.String(1))
    )

# Athlete
athlete = sqlalchemy.Table(
    "athlete",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(12), primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(128)),
    sqlalchemy.Column("last_name", sqlalchemy.String(128)),
    sqlalchemy.Column("gender", sqlalchemy.String(1)),
    sqlalchemy.Column("birth_year", sqlalchemy.Integer()),
    sqlalchemy.Column("lattest_noc", sqlalchemy.String(3))
    )

# AthleteView
athlete_view = sqlalchemy.Table(
    "athlete_view",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(12), primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(128)),
    sqlalchemy.Column("last_name", sqlalchemy.String(128)),
    sqlalchemy.Column("gender", sqlalchemy.String(1)),
    sqlalchemy.Column("birth_year", sqlalchemy.Integer),
    sqlalchemy.Column("nocs", sqlalchemy.ARRAY(sqlalchemy.String(3))),
    sqlalchemy.Column("disciplines", sqlalchemy.ARRAY(sqlalchemy.String(32))),
    sqlalchemy.Column("n_medals", sqlalchemy.Integer)
    )

# RegionView
region_view = sqlalchemy.Table(
    "region_view",
    metadata,
    sqlalchemy.Column("region", sqlalchemy.String(32)),
    sqlalchemy.Column("sport", sqlalchemy.String(32)),
    sqlalchemy.Column("season", sqlalchemy.String(6)),
    sqlalchemy.Column("year", sqlalchemy.Integer),
    sqlalchemy.Column("n_medals", sqlalchemy.Integer)
)

def main():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

if __name__ == "__main__":
    main()
