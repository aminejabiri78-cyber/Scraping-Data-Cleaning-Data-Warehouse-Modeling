from extract.scrape import scrape_avito
from staging.save_data import save_to_csv
from staging.save_data_db import *
import pandas as pd
def main():

    data = scrape_avito()

    df = pd.DataFrame(data)

    save_to_csv(df)
    save_db(df)

    print("✅ Pipeline finished successfully")


if __name__ == "__main__":
    main()