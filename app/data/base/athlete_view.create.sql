CREATE OR REPLACE VIEW athlete_view AS (
    SELECT first_name, last_name, gender, birth_year,
    ARRAY_AGG(DISTINCT result.noc) AS nocs,
    ARRAY_AGG(DISTINCT result.sport) AS disciplines,
    COUNT(medal) AS n_medals
    FROM athlete JOIN result
    ON athlete.id = result.athlete
    GROUP BY athlete.id
    ORDER BY n_medals DESC
                                        )
