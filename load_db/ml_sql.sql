
CREATE TABLE IF NOT EXISTS ml_schema.obt_table (
    titre TEXT,
    chambres INT,
    salle_de_bain INT,
    etage INT,
    prix NUMERIC,
    surface NUMERIC,
    prix_m2 NUMERIC,
    total_pieces INT,
    is_centre BOOLEAN,
    is_outlier BOOLEAN,
    ville TEXT,ER
    quartier TEXT,
    lien TEXT
);

TRUNCATE ml_schema.obt_table;

INSERT INTO ml_schema.obt_table (
    titre,
    chambres,
    salle_de_bain,
    etage,
    prix,
    surface,
    prix_m2,
    total_pieces,
    is_centre,
    is_outlier,
    ville,
    quartier,
    lien
    )
    SELECT
    p.titre,               
    p.chambres,
    p.salle_de_bain,
    p.etage,

    f.prix,                
    f.surface,
    f.prix_m2,
    f.total_pieces,
    f.is_centre,
    f.is_outlier,

    l.ville,                
    l.quartier,

    s.lien                  

    FROM BI_schema.fact_annonce f

    JOIN BI_schema.dim_property p 
    ON f.property_id = p.property_id

    JOIN BI_schema.dim_location l 
    ON f.location_id = l.location_id

    JOIN BI_schema.dim_source s 
    ON f.source_id = s.source_id;