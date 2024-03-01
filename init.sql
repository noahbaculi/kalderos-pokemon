CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY,
    pokemon_name TEXT,
    type1 TEXT,
    type2 TEXT,
    pokemon_order INTEGER,
    pokemon_weight INTEGER,
    height INTEGER
);

COPY pokemon(CAST(id AS INTEGER) AS id, pokemon_name, type1, type2, pokemon_order, pokemon_weight, height)
FROM '/var/lib/postgresql/data/pokemon.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE pokemon_types (
    id INTEGER,
    type TEXT,
    damage_modifier TEXT,
    target_types TEXT
);

COPY pokemon_types(id, type, damage_modifier, target_types)
FROM '/var/lib/postgresql/data/pokemon_types.csv' DELIMITER ',' CSV HEADER;
