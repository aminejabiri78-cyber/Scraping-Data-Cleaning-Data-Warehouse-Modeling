import pandas as pd


def save_to_csv(data):
    df = pd.DataFrame(data)

    url = r"C:\Users\AMINE JBR\Documents\Scraping-Data-Cleaning-Data-Warehouse-Modeling\data\avito_appartements.csv"

    df.to_csv(url, index=False, encoding="utf-8-sig")

    print("Scraping terminé !")
    print(df.head())
