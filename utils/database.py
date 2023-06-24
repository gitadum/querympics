#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2

def create(db_name,
           query,
           connector: psycopg2.connection,
           cursor: psycopg2.cursor,
           verbose = True):
    print(f"Crating `{db_name}`...") if verbose else None
    cursor.execute(query)
    connector.commit()
    print(f"Created `{db_name}`.") if verbose else None
