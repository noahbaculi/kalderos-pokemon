from io import StringIO
from sqlalchemy import create_engine
import typer
import pandas as pd

app = typer.Typer()


def load_table_data(
    csv_path: str,
    table_name: str,
    str_cols: list[str] = [],
    int16_cols: list[str] = [],
    categorical_cols: list[str] = [],
) -> None:
    print(f"Loading table data for {table_name}...")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names
    df.id = df.id.astype(int)  # Will raise exception if not all ids are integers

    # Convert columns to nullable string type
    for col in str_cols:
        df[col] = df[col].astype(pd.StringDtype())

    # Convert columns to categorical type
    for col in categorical_cols:
        df[col] = df[col].astype(pd.CategoricalDtype())

    # Convert columns to to nullable Int16 type
    # ** Assuming values will never exceed Int16 range
    for col in int16_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype(pd.Int16Dtype())

    # Use StingIO buffer to copy data to PostgreSQL
    buffer = StringIO()
    df.to_csv(buffer, header=False, index=False)
    buffer.seek(0)
    try:
        raw_connection = CONNECTION.connection
        cursor = raw_connection.cursor()
        cursor.copy_from(buffer, table_name, sep=",", null="")
        raw_connection.commit()
    except Exception as error:
        print("Error: %s" % error)
        raw_connection.rollback()


@app.command()
def setup():
    load_table_data(
        "./dataset/pokemon.csv",
        table_name="pokemon",
        str_cols=["name"],
        int16_cols=["order", "weight", "height"],
        categorical_cols=["type1", "type2"],
    )
    load_table_data(
        "./dataset/pokemon_types.csv",
        table_name="pokemon_types",
        categorical_cols=["type", "damage_modifier", "target_types"],
    )


@app.command()
def run1():
    print('"Which Pokemon can effectively battle the most number of Pokemon with 4x effectiveness?"')

    SQL = """
    WITH pokemon_effectiveness AS (
        SELECT
            type AS attacking_type
            , target_types AS defending_type
            , damage_modifier
            , CASE damage_modifier
                WHEN 'no_damage_to' THEN 0
                WHEN 'half_damage_to' THEN 0.5
                WHEN 'double_damage_to' THEN 2
            ELSE 1 END AS effectiveness
        FROM pokemon_types
    )
    , combined_effectiveness AS (
        SELECT
            pokemon_effectiveness_1.attacking_type
            , pokemon_effectiveness_1.defending_type AS defending_type_1
            , pokemon_effectiveness_1.effectiveness AS effectiveness_1
            , pokemon_effectiveness_2.defending_type AS defending_type_2
            , pokemon_effectiveness_2.effectiveness AS effectiveness_2
            , (pokemon_effectiveness_1.effectiveness * pokemon_effectiveness_2.effectiveness) AS combined_effectiveness
        FROM pokemon_effectiveness AS pokemon_effectiveness_1
        CROSS JOIN (
            SELECT * FROM pokemon_effectiveness
            UNION ALL
            SELECT NULL , NULL , NULL , 1
        ) AS pokemon_effectiveness_2
        WHERE
            (
                pokemon_effectiveness_1.attacking_type = pokemon_effectiveness_2.attacking_type
                OR pokemon_effectiveness_2.attacking_type IS NULL
            )
            AND
            (
                pokemon_effectiveness_1.defending_type < pokemon_effectiveness_2.defending_type
                OR pokemon_effectiveness_2.defending_type IS NULL
            )
        ORDER BY
            attacking_type
            , defending_type_1
            , defending_type_2
            , combined_effectiveness
    )
    , battles AS (
        SELECT
            p_attacking.name AS attacking_name
            , p_attacking.type1 AS attacking_type_1
            , p_attacking.type2 AS attacking_type_2
            , p_defending.name AS defending_name
            , p_defending.type1 AS defending_type_1
            , p_defending.type2 AS defending_type_2
            , combined_effectiveness.effectiveness_1
            , combined_effectiveness.effectiveness_2
            , combined_effectiveness.combined_effectiveness
        FROM pokemon AS p_attacking
        CROSS JOIN pokemon AS p_defending
        JOIN combined_effectiveness
            ON (
                p_attacking.type1 = combined_effectiveness.attacking_type
                OR p_attacking.type2 = combined_effectiveness.attacking_type
            )
            AND p_defending.type1 = combined_effectiveness.defending_type_1
            AND (
                ( p_defending.type2 IS NULL AND combined_effectiveness.defending_type_2 IS NULL )
                OR p_defending.type2 = combined_effectiveness.defending_type_2
            )
        WHERE
            p_attacking.id != p_defending.id
            
        ORDER BY
            p_attacking.name
            , p_defending.name
            , combined_effectiveness.combined_effectiveness
    )
    SELECT
        attacking_name
        , COUNT(DISTINCT defending_name) AS number_of_effective_battles
    FROM battles
    WHERE
        combined_effectiveness = 4
    GROUP BY
        attacking_name
    ORDER BY number_of_effective_battles DESC
    """

    df = pd.read_sql(SQL, CONNECTION)
    print(df.head(5).to_markdown(index=False))


@app.command()
def run2():
    print('"Which Pokemon can effectively battle the most number of Pokemon with at least 2x effectiveness?"')

    SQL = """
    WITH pokemon_effectiveness AS (
        SELECT
            type AS attacking_type
            , target_types AS defending_type
            , damage_modifier
            , CASE damage_modifier
                WHEN 'no_damage_to' THEN 0
                WHEN 'half_damage_to' THEN 0.5
                WHEN 'double_damage_to' THEN 2
            ELSE 1 END AS effectiveness
        FROM pokemon_types
    )
    , combined_effectiveness AS (
        SELECT
            pokemon_effectiveness_1.attacking_type
            , pokemon_effectiveness_1.defending_type AS defending_type_1
            , pokemon_effectiveness_1.effectiveness AS effectiveness_1
            , pokemon_effectiveness_2.defending_type AS defending_type_2
            , pokemon_effectiveness_2.effectiveness AS effectiveness_2
            , (pokemon_effectiveness_1.effectiveness * pokemon_effectiveness_2.effectiveness) AS combined_effectiveness
        FROM pokemon_effectiveness AS pokemon_effectiveness_1
        CROSS JOIN (
            SELECT * FROM pokemon_effectiveness
            UNION ALL
            SELECT NULL , NULL , NULL , 1
        ) AS pokemon_effectiveness_2
        WHERE
            (
                pokemon_effectiveness_1.attacking_type = pokemon_effectiveness_2.attacking_type
                OR pokemon_effectiveness_2.attacking_type IS NULL
            )
            AND
            (
                pokemon_effectiveness_1.defending_type < pokemon_effectiveness_2.defending_type
                OR pokemon_effectiveness_2.defending_type IS NULL
            )
        ORDER BY
            attacking_type
            , defending_type_1
            , defending_type_2
            , combined_effectiveness
    )
    , battles AS (
        SELECT
            p_attacking.name AS attacking_name
            , p_attacking.type1 AS attacking_type_1
            , p_attacking.type2 AS attacking_type_2
            , p_defending.name AS defending_name
            , p_defending.type1 AS defending_type_1
            , p_defending.type2 AS defending_type_2
            , combined_effectiveness.effectiveness_1
            , combined_effectiveness.effectiveness_2
            , combined_effectiveness.combined_effectiveness
        FROM pokemon AS p_attacking
        CROSS JOIN pokemon AS p_defending
        JOIN combined_effectiveness
            ON (
                p_attacking.type1 = combined_effectiveness.attacking_type
                OR p_attacking.type2 = combined_effectiveness.attacking_type
            )
            AND p_defending.type1 = combined_effectiveness.defending_type_1
            AND (
                ( p_defending.type2 IS NULL AND combined_effectiveness.defending_type_2 IS NULL )
                OR p_defending.type2 = combined_effectiveness.defending_type_2
            )
        WHERE
            p_attacking.id != p_defending.id
            
        ORDER BY
            p_attacking.name
            , p_defending.name
            , combined_effectiveness.combined_effectiveness
    )
    SELECT
        attacking_name
        , COUNT(DISTINCT defending_name) AS number_of_effective_battles
    FROM battles
    WHERE
        combined_effectiveness >= 2
    GROUP BY
        attacking_name
    ORDER BY number_of_effective_battles DESC
    """

    df = pd.read_sql(SQL, CONNECTION)
    print(df.head(5).to_markdown(index=False))


@app.command()
def run3():
    print(
        "Which Pokemon can resist the most number of attacking Pokemon?"
        " (meaning it can resist at least 1 of the types of attacking Pokemon?)"
    )

    SQL = """
    WITH pokemon_effectiveness AS (
        SELECT
            type AS attacking_type
            , target_types AS defending_type
            , damage_modifier
            , CASE damage_modifier
                WHEN 'no_damage_to' THEN 0
                WHEN 'half_damage_to' THEN 0.5
                WHEN 'double_damage_to' THEN 2
            ELSE 1 END AS effectiveness
        FROM pokemon_types
    )
    , combined_effectiveness AS (
        SELECT
            pokemon_effectiveness_1.attacking_type
            , pokemon_effectiveness_1.defending_type AS defending_type_1
            , pokemon_effectiveness_1.effectiveness AS effectiveness_1
            , pokemon_effectiveness_2.defending_type AS defending_type_2
            , pokemon_effectiveness_2.effectiveness AS effectiveness_2
            , (pokemon_effectiveness_1.effectiveness * pokemon_effectiveness_2.effectiveness) AS combined_effectiveness
        FROM pokemon_effectiveness AS pokemon_effectiveness_1
        CROSS JOIN (
            SELECT * FROM pokemon_effectiveness
            UNION ALL
            SELECT NULL , NULL , NULL , 1
        ) AS pokemon_effectiveness_2
        WHERE
            (
                pokemon_effectiveness_1.attacking_type = pokemon_effectiveness_2.attacking_type
                OR pokemon_effectiveness_2.attacking_type IS NULL
            )
            AND
            (
                pokemon_effectiveness_1.defending_type < pokemon_effectiveness_2.defending_type
                OR pokemon_effectiveness_2.defending_type IS NULL
            )
        ORDER BY
            attacking_type
            , defending_type_1
            , defending_type_2
            , combined_effectiveness
    )
    , battles AS (
        SELECT
            p_attacking.name AS attacking_name
            , p_attacking.type1 AS attacking_type_1
            , p_attacking.type2 AS attacking_type_2
            , p_defending.name AS defending_name
            , p_defending.type1 AS defending_type_1
            , p_defending.type2 AS defending_type_2
            , combined_effectiveness.effectiveness_1
            , combined_effectiveness.effectiveness_2
            , combined_effectiveness.combined_effectiveness
        FROM pokemon AS p_attacking
        CROSS JOIN pokemon AS p_defending
        JOIN combined_effectiveness
            ON (
                p_attacking.type1 = combined_effectiveness.attacking_type
                OR p_attacking.type2 = combined_effectiveness.attacking_type
            )
            AND p_defending.type1 = combined_effectiveness.defending_type_1
            AND (
                ( p_defending.type2 IS NULL AND combined_effectiveness.defending_type_2 IS NULL )
                OR p_defending.type2 = combined_effectiveness.defending_type_2
            )
        WHERE
            p_attacking.id != p_defending.id
            
        ORDER BY
            p_attacking.name
            , p_defending.name
            , combined_effectiveness.combined_effectiveness
    )
    , resistances AS (
        SELECT
            attacking_name
            , defending_name
            , MAX(
                CASE WHEN (effectiveness_1 < 1) OR (effectiveness_2 < 1) THEN 1 ELSE 0 END
            ) AS resistance
        FROM battles
        GROUP BY
            attacking_name
            , defending_name
    )
    SELECT
        defending_name
        , COUNT(DISTINCT attacking_name) AS number_of_resistances
    FROM resistances
    GROUP BY
        defending_name
    ORDER BY
        number_of_resistances DESC
    """

    df = pd.read_sql(SQL, CONNECTION)
    print(df.head(10).to_markdown(index=False))


@app.command()
def run_all():
    run1()
    print()
    run2()
    print()
    run3()
    print()


if __name__ == "__main__":
    # Connect to PostgreSQL
    engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost/myuser")
    with engine.connect() as CONNECTION:
        app()

    engine.dispose()
