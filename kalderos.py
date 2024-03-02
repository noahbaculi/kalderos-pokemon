from io import StringIO
import psycopg2
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
        CURSOR.copy_from(buffer, table_name, sep=",", null="")
        CONNECTION.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        CONNECTION.rollback()


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

    breakpoint()

    # Execute SQL queries
    CURSOR.execute("SELECT * FROM pokemon;")
    print(f"{CURSOR.statusmessage = }")
    rows = CURSOR.fetchall()
    for row in rows:
        print(row)


def run():
    print("Running!")


if __name__ == "__main__":
    # Connect to PostgreSQL
    with psycopg2.connect(
        dbname="myuser",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432",
    ) as CONNECTION:
        # Create database cursor
        with CONNECTION.cursor() as CURSOR:
            app()
