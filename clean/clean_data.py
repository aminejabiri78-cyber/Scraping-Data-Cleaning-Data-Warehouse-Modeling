from sqlalchemy import engine,create_engine,text
import pandas as pd 
from dotenv import load_dotenv
import os 

load_dotenv()
USER = os.getenv("USER")
PASS = os.getenv("PASS")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB_NAME")
try:
    url=f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
    engine=create_engine(url)
    with engine.begin() as con :
        rs=con.execute(text("select * from  version();"))
        db_ver=rs.fetchone()
        print(f" Database connected: {db_ver}")
except Exception as e:
    print(f" error: {e}")

with engine.begin() as con :
    df=pd.read_sql("SELECT * FROM staging.avito_raw",engine)
   
