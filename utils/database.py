#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import psycopg2
import sqlalchemy

def create(db_name,
           query_file_path,
           connector: psycopg2.connection,
           cursor: psycopg2.cursor,
           verbose = True):
    print(f"Crating `{db_name}`...") if verbose else None
    with open(query_file_path, "r") as f:
        query = f.read()
    query = query.split(";")[0]
    cursor.execute(query)
    connector.commit()
    print(f"Created `{db_name}`.") if verbose else None

def truncate(db_name,
             query,
             connector: psycopg2.connection,
             cursor: psycopg2.cursor,
             verbose = True):
    print(f"Truncating `{db_name}`...") if verbose else None
    cursor.execute(query)
    connector.commit()
    print("Truncated `{db_name}`.") if verbose else None

def fill_table_from_csv(db_name,
                        file_path,
                        connector: psycopg2.connection,
                        engine: sqlalchemy.Engine,
                        verbose = True,
                        fill_by_chuncks = False,
                        n_chunk = 10000):
    
    print(f"Starting loading records into `{db_name}`...") if verbose else None
    if fill_by_chuncks:
        # Remplissage de la table par lot
        # la taille d'un lot est déterminé par "n_chunk"
        i = 0
        for chunk in pd.read_csv(file_path, chunksize=n_chunk):
            chunk.to_sql(db_name, engine, if_exists="append", index=False)
            i += n_chunk
            print(f"loaded {i} records into {db_name}.") if verbose else None
    else:
        # Remplissage de la table en une seule fois
        df = pd.read_csv(file_path)
        df.to_sql(db_name, engine, if_exists="append", index=False)
    connector.commit()
    print("Done with loading records into `athlete`.") if verbose else None
