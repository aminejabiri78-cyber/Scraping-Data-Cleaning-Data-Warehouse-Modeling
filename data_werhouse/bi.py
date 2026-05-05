from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

def load_to_bi():

    load_dotenv()

    USER = os.getenv("USER")
    PASS = os.getenv("PASS")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    DB_NAME = os.getenv("DB_NAME")

    # -------------------------
    # CONNECTION SAFE
    # -------------------------
    try:
        url = f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
        engine = create_engine(url)

        with engine.begin() as con:
            ver = con.execute(text("select version();")).fetchone()
            print(f"✅ DB connected: {ver}")

    except Exception as e:
        print(f"❌ connection error: {e}")
        return

    # -------------------------
    # CREATE SCHEMA
    # -------------------------
    with engine.begin() as con:
        con.execute(text("CREATE SCHEMA IF NOT EXISTS bi_schema;"))

        with open(r"C:\Users\user\Documents\scraping_avito\load_db\bi_sql.sql", "r", encoding="utf-8") as f:
            con.exec_driver_sql(f.read())

    print("✅ schema created")

    # -------------------------
    # LOAD DATA ONCE ONLY (FIX)
    # -------------------------
    df = pd.read_sql("SELECT * FROM clean.avito_clean", engine)
    df.columns = df.columns.str.lower()

    # -------------------------
    # DIM LOCATION
    # -------------------------
    dim_location = df[["ville", "quartier"]].drop_duplicates()
    dim_location.to_sql("dim_location", engine, schema="bi_schema", if_exists="append", index=False)

    # -------------------------
    # DIM SOURCE
    # -------------------------
    dim_source = df[["lien"]].drop_duplicates()
    dim_source.to_sql("dim_source", engine, schema="bi_schema", if_exists="append", index=False)

    # -------------------------
    # DIM PROPERTY
    # -------------------------
    dim_property = df[["titre", "chambres", "salle_de_bain", "etage"]].drop_duplicates()
    dim_property.to_sql("dim_property", engine, schema="bi_schema", if_exists="append", index=False)

    # -------------------------
    # RELOAD DIM TABLES
    # -------------------------
    dim_location_db = pd.read_sql("SELECT * FROM bi_schema.dim_location", engine)
    dim_property_db = pd.read_sql("SELECT * FROM bi_schema.dim_property", engine)
    dim_source_db = pd.read_sql("SELECT * FROM bi_schema.dim_source", engine)

    # -------------------------
    # MERGE SAFE
    # -------------------------
    df = df.merge(dim_location_db, on=["ville", "quartier"], how="left")
    df = df.merge(dim_property_db, on=["titre", "chambres", "salle_de_bain", "etage"], how="left")
    df = df.merge(dim_source_db, on="lien", how="left")

    # -------------------------
    # FACT TABLE
    # -------------------------
    fact_annonce = df[[
        "location_id",
        "property_id",
        "source_id",
        "prix",
        "surface",
        "prix_m2",
        "total_pieces",
        "is_centre",
        "is_outlier"
    ]].drop_duplicates()

    fact_annonce.to_sql(
        "fact_annonce",
        engine,
        schema="bi_schema",
        if_exists="append",
        index=False
    )

    print("🚀 BI load terminé avec succès !")