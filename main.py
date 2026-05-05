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
    df_clean = clean_data(df)

    # 4. DB ENGINE
    load_dotenv()
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASS')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
    )

    # 5. SAVE CLEAN
    save_clean_data(df_clean, engine, "data/avito_clean.csv")

    # 6. BI LAYER
    load_to_bi(df_clean, engine)
    print("🚀 Pipeline finished successfully")


if __name__ == "__main__":
    main()