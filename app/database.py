#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import databases
import sqlalchemy

from datetime import datetime

# # BASE DE DONNÉES  # #

db_usr = "sqladum"
db_pwd = "dummypassw0rd"
db_name = "olympics"
db_host = "localhost"
db_port = 5432

DATABASE_URL = f"postgresql://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

def main():
    # Result
    result = sqlalchemy.table(
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
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

if __name__ == "__main__":
    main()
