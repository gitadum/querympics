CREATE TABLE IF NOT EXISTS athlete (
    id CHAR(12) PRIMARY KEY,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    gender CHAR,
    birth_year INT,
    lattest_noc CHAR(3)
);