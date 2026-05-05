import pandas as pd
from sqlalchemy import text

# -------------------------
# CLEAN FUNCTION
# -------------------------
def clean_data(df):

    def clean_numeric(col):
        return pd.to_numeric(
            col.astype(str).str.replace(r"\D", "", regex=True),
            errors="coerce"
        )

    # Drop duplicates
    df = df.drop_duplicates(subset=["lien"])

    # Clean columns
    df.columns = df.columns.str.strip().str.capitalize()

    # Numeric
    for col in ["Prix", "Surface", "Chambres", "Salle_de_bain", "Etage"]:
        df[col] = clean_numeric(df[col])

    # Ville
    df["Ville"] = (
        df["Ville"]
        .astype(str)
        .str.replace("Appartements dans", "")
        .str.strip()
    )

    df[["Ville", "Quartier"]] = df["Ville"].str.split(",", n=1, expand=True)
    df["Quartier"] = df["Quartier"].fillna("Unknown")

    # Fill nulls
    df["Chambres"] = df["Chambres"].fillna(0)
    df["Salle_de_bain"] = df["Salle_de_bain"].fillna(0)
    df["Etage"] = df["Etage"].fillna(0)

    # Remove invalid
    df = df.dropna(subset=["Prix", "Surface", "Ville"])
    df = df[(df["Prix"] > 0) & (df["Surface"] > 0)]

    # Features
    df["Prix_m2"] = df["Prix"] / df["Surface"]
    df["Total_pieces"] = df["Chambres"] + df["Salle_de_bain"]
    df["Is_centre"] = df["Quartier"].str.contains("centre", case=False, na=False)

    # Outliers
    def add_outlier_flags(df, col):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        return (df[col] < lower) | (df[col] > upper)

    df["Is_outlier"] = (
        add_outlier_flags(df, "Prix") |
        add_outlier_flags(df, "Surface") |
        add_outlier_flags(df, "Prix_m2")
    )

    return df


# -------------------------
# SAVE FUNCTION
# -------------------------
def save_data(df, engine, path):

    with engine.begin() as con:
        con.execute(text("CREATE SCHEMA IF NOT EXISTS clean"))

    df.to_sql(
        "avito_appartements_clean",
        engine,
        schema="clean",
        if_exists="replace",
        index=False
    )

    df.to_csv(path, index=False)

    print("✅ Data saved (DB + CSV)")