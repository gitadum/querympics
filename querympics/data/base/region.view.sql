CREATE OR REPLACE VIEW region_view AS (
    SELECT region.region, result.sport, games.season, games.year,
    COUNT(medal) AS n_medals
    FROM result
    JOIN games ON result.games = games.id
    JOIN region ON result.noc = region.noc 
    GROUP BY result.noc, region.region, result.sport, games.season, games.year
    ORDER BY n_medals DESC
                                        )