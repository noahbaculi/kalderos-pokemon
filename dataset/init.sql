-- NOTE: Could use ENUM type for many fields with more domain knowledge

CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type1 TEXT,  
    type2 TEXT,
    "order" SMALLINT NULL,
    "weight" SMALLINT NULL,
    height SMALLINT NULL
);

CREATE TABLE pokemon_types (
    id INTEGER,
    "type" TEXT,
    damage_modifier TEXT,
    target_types TEXT
);
