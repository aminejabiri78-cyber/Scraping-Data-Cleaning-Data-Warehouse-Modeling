from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER")
PASS = os.getenv("PASS")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB_NAME")


try:
    url = f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
    engine = create_engine(url)

    with engine.connect() as con:
        rs = con.execute(text("SELECT version();"))
        db_version = rs.fetchone()
        print(f" Database connected: {db_version}")

except Exception as e:
    print(f" error: {e}")


with engine.begin() as con:
    con.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))

    con.execute(text("""
        CREATE TABLE IF NOT EXISTS staging.avito_raw (
            titre TEXT,
            prix TEXT,
            ville TEXT,
            surface TEXT,
            chambres TEXT,
            salle_de_bain TEXT,
            etage TEXT,
            lien TEXT
        )
    """))

print("staging ready")



def save_db(data):
    df = pd.DataFrame(data)

    df.to_sql(
        "avito_raw",
        engine,
        schema="staging",
        if_exists="append",
        index=False
    )

    print(" Data inserted into staging DB")