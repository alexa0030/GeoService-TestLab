"""Download a reproducible Shanghai OSM extract and load three PostGIS layers.

Data © OpenStreetMap contributors, available under the ODbL.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import psycopg
import requests


OVERPASS_ENDPOINTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.nchc.org.tw/api/interpreter",
)
DEFAULT_BBOX = "31.18,121.40,31.30,121.56"  # south,west,north,east
ROOT = Path(__file__).resolve().parents[1]


def query_osm(bbox: str, timeout: int = 300) -> dict:
    selectors = ('way["building"]', 'way["highway"]', 'node["amenity"]')
    elements = []
    headers = {
        "User-Agent": "GeoService-TestLab/1.0 (+https://github.com/alexa0030/GeoService-TestLab)"
    }
    for selector in selectors:
        query = f"[out:json][timeout:240];{selector}({bbox});out tags geom;"
        errors = []
        for endpoint in OVERPASS_ENDPOINTS:
            try:
                response = requests.get(
                    endpoint, params={"data": query}, headers=headers, timeout=timeout,
                )
                response.raise_for_status()
                elements.extend(response.json().get("elements", []))
                time.sleep(1)
                break
            except (requests.RequestException, ValueError) as error:
                errors.append(f"{endpoint}: {error}")
        else:
            raise RuntimeError(
                f"All Overpass endpoints failed for {selector}: " + " | ".join(errors)
            )
    return {"elements": elements}


def classify(payload: dict) -> dict[str, list[tuple]]:
    layers: dict[str, list[tuple]] = {"buildings": [], "roads": [], "pois": []}
    for element in payload.get("elements", []):
        tags = element.get("tags", {})
        osm_id = int(element["id"])
        if element["type"] == "node" and "amenity" in tags:
            geometry = {"type": "Point", "coordinates": [element["lon"], element["lat"]]}
            layers["pois"].append((osm_id, tags.get("name"), tags["amenity"], geometry, tags))
            continue
        coordinates = [[point["lon"], point["lat"]] for point in element.get("geometry", [])]
        if len(coordinates) < 2:
            continue
        if "building" in tags and len(coordinates) >= 4:
            if coordinates[0] != coordinates[-1]:
                coordinates.append(coordinates[0])
            geometry = {"type": "Polygon", "coordinates": [coordinates]}
            layers["buildings"].append((osm_id, tags.get("name"), tags["building"], geometry, tags))
        elif "highway" in tags:
            geometry = {"type": "LineString", "coordinates": coordinates}
            layers["roads"].append((osm_id, tags.get("name"), tags["highway"], geometry, tags))
    return layers


def load_postgis(layers: dict[str, list[tuple]], dsn: str) -> None:
    definitions = {
        "buildings": ("building_type", "Polygon"),
        "roads": ("highway_type", "LineString"),
        "pois": ("amenity_type", "Point"),
    }
    with psycopg.connect(dsn) as connection:
        with connection.cursor() as cursor:
            for layer, rows in layers.items():
                category, geometry_type = definitions[layer]
                table = f"osm_{layer}"
                cursor.execute(f"DROP TABLE IF EXISTS public.{table}")
                cursor.execute(f"""
                    CREATE TABLE public.{table} (
                      osm_id bigint PRIMARY KEY, name text, {category} text NOT NULL,
                      tags jsonb NOT NULL, geom geometry({geometry_type}, 4326) NOT NULL)
                """)
                cursor.executemany(f"""
                    INSERT INTO public.{table} (osm_id, name, {category}, geom, tags)
                    VALUES (%s, %s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326), %s)
                """, [
                    (osm_id, name, kind, json.dumps(geometry), json.dumps(tags))
                    for osm_id, name, kind, geometry, tags in rows
                ])
                cursor.execute(f"CREATE INDEX {table}_geom_idx ON public.{table} USING gist (geom)")
                cursor.execute(f"ANALYZE public.{table}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bbox", default=DEFAULT_BBOX)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/osm_data_stats.json")
    args = parser.parse_args()
    if args.snapshot:
        payload = json.loads(args.snapshot.read_text(encoding="utf-8"))
        source = str(args.snapshot)
    else:
        payload = query_osm(args.bbox)
        source = "Overpass API / OpenStreetMap"
    layers = classify(payload)
    empty = [name for name, rows in layers.items() if not rows]
    if empty:
        raise RuntimeError(f"No usable features for layers: {', '.join(empty)}")
    load_postgis(
        layers,
        os.getenv("DATABASE_URL", "postgresql://geoservice:geoservice@localhost:5432/geoservice"),
    )
    stats = {
        "source": source,
        "license": "ODbL 1.0",
        "attribution": "© OpenStreetMap contributors",
        "bbox": args.bbox,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "feature_counts": {name: len(rows) for name, rows in layers.items()},
        "total_features": sum(map(len, layers.values())),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
