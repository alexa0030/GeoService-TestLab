CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS public.sample_features (
    id integer PRIMARY KEY,
    name text NOT NULL,
    urban_level text NOT NULL,
    geom geometry(Polygon, 4326) NOT NULL
);

INSERT INTO public.sample_features (id, name, urban_level, geom) VALUES
  (1, 'Central Urban', 'urban', ST_GeomFromText('POLYGON((121.35 31.15,121.55 31.15,121.55 31.35,121.35 31.35,121.35 31.15))', 4326)),
  (2, 'Urban Fringe', 'peri-urban', ST_GeomFromText('POLYGON((121.55 31.15,121.75 31.15,121.75 31.35,121.55 31.35,121.55 31.15))', 4326)),
  (3, 'Rural Sample', 'rural', ST_GeomFromText('POLYGON((121.75 31.15,121.95 31.15,121.95 31.35,121.75 31.35,121.75 31.15))', 4326))
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  urban_level = EXCLUDED.urban_level,
  geom = EXCLUDED.geom;

CREATE INDEX IF NOT EXISTS sample_features_geom_idx
ON public.sample_features USING gist (geom);

