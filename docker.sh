#! /bin/bash
docker pull postgres:alpine
docker run --name postgres-alpine -e POSTGRES_USER=sqladum -e POSTGRES_PASSWORD=dummypassw0rd -d -p 5432:5432 postgres:alpine
docker exec -it postgres-alpine bash
psql -U sqladum
CREATE DATABASE olympics;

psql -h localhost -p 5432 -U sqladum
\c olympics
\q
