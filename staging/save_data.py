import pandas as pd


def save_to_csv(data):
    df = pd.DataFrame(data)

    url = r"C:\Users\user\Documents\scraping_avito\data\avito_appartements.csv"

    df.to_csv(url, index=False, encoding="utf-8-sig")

    print("Scraping terminé !")
    print(df.head())
