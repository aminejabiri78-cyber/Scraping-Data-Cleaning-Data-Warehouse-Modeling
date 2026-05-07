from extract.scrape import scrape_avito
from staging.save_data import save_to_csv
from staging.save_data_db import save_db
from clean.clean_data import clean_data, save_data as save_clean_data
from data_werhouse.bi import load_to_bi
from data_werhouse.ml_schema import load_ml_schema
from data_werhouse.db import get_engine

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
    df_clean = clean_data(df)

    # 4. DB ENGINE
    engine = get_engine()

    

    # 5. SAVE CLEAN
    save_clean_data(df_clean, engine, "data/avito_clean.csv")

    # 6. BI LAYER
    load_to_bi(df_clean, engine)
    load_ml_schema()
    print(" Pipeline finished successfully")


if __name__ == "__main__":
    main()
