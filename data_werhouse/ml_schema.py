from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER")
PASS = os.getenv("PASS")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB_NAME")


def load_ml_schema():
    try:
        url = f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
        engine = create_engine(url)

        with engine.connect() as con:
            rs = con.execute(text("SELECT version();"))
            print(f"Database connected: {rs.fetchone()}")

        with engine.begin() as con:
            con.execute(text("CREATE SCHEMA IF NOT EXISTS ml_schema;"))

            with open(
                r"C:\Users\AMINE JBR\Documents\Scraping-Data-Cleaning-Data-Warehouse-Modeling\load_db\ml_sql.sql",
                "r",
                encoding="utf-8"
            ) as f:
                con.exec_driver_sql(f.read())


    except Exception as e:
        print(f"Error loading ML schema: {e}")