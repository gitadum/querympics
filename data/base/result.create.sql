CREATE TABLE IF NOT EXISTS result (
    id CHAR(7) PRIMARY KEY,
    games CHAR(5),
    sport VARCHAR(32),
    event VARCHAR(128),
    athlete CHAR(12),
    noc CHAR(3),
    medal CHAR
)
