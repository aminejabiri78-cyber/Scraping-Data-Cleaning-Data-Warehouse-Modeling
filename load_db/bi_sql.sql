CREATE TABLE BI_schema.dim_location (
    location_id SERIAL PRIMARY KEY,
    ville VARCHAR(100),
    quartier VARCHAR(150)
);

CREATE TABLE BI_schema.dim_source (
    source_id SERIAL PRIMARY KEY,
    lien TEXT
);

CREATE TABLE BI_schema.dim_property (
    property_id SERIAL PRIMARY KEY,
    titre TEXT,
    chambres INT,
    salle_de_bain INT,
    etage INT
);

CREATE TABLE BI_schema.fact_annonce (
    annonce_id SERIAL PRIMARY KEY,

    location_id INT REFERENCES BI_schema.dim_location(location_id),
    property_id INT REFERENCES BI_schema.dim_property(property_id),
    source_id INT REFERENCES BI_schema.dim_source(source_id),

    prix NUMERIC,
    surface NUMERIC,
    prix_m2 NUMERIC,
    total_pieces INT,

    is_centre BOOLEAN,
    is_outlier BOOLEAN
);