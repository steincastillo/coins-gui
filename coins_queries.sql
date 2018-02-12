-- full DB query
select name, value, year, currency from coins
inner join country on country.iso = coins.country;

-- Full DB query V2.0
select
name as country,
value,
year,
currency 
from
coins
INNER JOIN country on country.iso = coins.country;

-- Full DB query V2.2
SELECT 
    name as country,
    value,
    year,
    currency 
FROM
    coins
INNER JOIN country on country.iso = coins.country
ORDER BY year;

-- Create DB view
CREATE VIEW IF NOT EXISTS v_coins AS 
    SELECT 
        name as country,
        value,
        year,
        currency
    FROM 
        coins
    INNER JOIN country on country.iso = coins.country
    ORDER BY year;

