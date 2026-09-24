import json
import os
from pathlib import Path

import psycopg


root = Path(__file__).resolve().parents[1]
features = json.loads((root / "data/sample.geojson").read_text(encoding="utf-8"))["features"]
dsn = os.getenv("DATABASE_URL", "postgresql://geoservice:geoservice@localhost:5432/geoservice")
with psycopg.connect(dsn) as connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.sample_features (
              id integer PRIMARY KEY, name text NOT NULL, urban_level text NOT NULL,
              geom geometry(Polygon, 4326) NOT NULL)
        """)
        for feature in features:
            props = feature["properties"]
            cursor.execute("""
                INSERT INTO public.sample_features (id, name, urban_level, geom)
                VALUES (%s, %s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))
                ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name,
                  urban_level=EXCLUDED.urban_level, geom=EXCLUDED.geom
            """, (props["id"], props["name"], props["urban_level"], json.dumps(feature["geometry"])))

