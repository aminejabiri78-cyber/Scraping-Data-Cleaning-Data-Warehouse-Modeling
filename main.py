from extract.scrape import scrape_avito
from staging.save_data import save_to_csv
from staging.save_data_db import save_db
from clean.clean_data import clean_data, save_data as save_clean_data
from data_werhouse.bi import load_to_bi
from sqlalchemy import create_engine
import pandas as pd
import os 
from dotenv import load_dotenv

def main():

    # 1. EXTRACT
    
    data = scrape_avito()
    df = pd.DataFrame(data)

    # 2. STAGING 
    save_to_csv(df)
    save_db(df)  

    # 3. CLEAN
    
    df = clean_data(df)

    # 4. DB ENGINE (FIXED)
    load_dotenv()
    engine = create_engine(f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASS')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}")
    # 5. LOAD CLEAN DATA
    save_clean_data(df, engine, path="data/avito_appartements_clean.csv")
    save_db(df)  
    load_to_bi()
    print("Pipeline finished successfully")


if __name__ == "__main__":
    main()