# Shanghai open-data source

The scaled benchmark uses an OpenStreetMap extract for central Shanghai
(`31.18,121.40,31.30,121.56`) and derives three geometry workloads:

- `osm_buildings` — polygon features and comparatively expensive geometry;
- `osm_roads` — line features with varied vertex counts;
- `osm_pois` — amenity points and a lightweight comparison layer.

Data is fetched through the Overpass API by `scripts/load_shanghai_osm.py`.
The script stores the retrieval timestamp, bounding box and actual feature
counts in `reports/osm_data_stats.json`, then creates spatial indexes and runs
PostgreSQL `ANALYZE`.

## License and attribution

Contains information from OpenStreetMap, which is made available at
[openstreetmap.org](https://www.openstreetmap.org/copyright) under the Open
Database License (ODbL). **© OpenStreetMap contributors.** BBBike is the
preferred city-extract fallback and distributes its OSM extracts under the same
OpenStreetMap license.

Raw data is not committed to Git. This avoids an unnecessarily large repository
and ensures that redistributed derivative data is not accidentally detached
from its required attribution and ODbL notice.

