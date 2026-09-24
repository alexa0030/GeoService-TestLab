from scripts.load_shanghai_osm import classify, split_bbox


def test_split_bbox_creates_complete_grid():
    tiles = split_bbox("31.18,121.40,31.30,121.56")
    assert len(tiles) == 16
    assert tiles[0] == "31.180000,121.400000,31.210000,121.440000"
    assert tiles[-1] == "31.270000,121.520000,31.300000,121.560000"


def test_classify_osm_geometry_layers():
    payload = {"elements": [
        {"type": "node", "id": 1, "lat": 31.2, "lon": 121.5,
         "tags": {"amenity": "school", "name": "Demo"}},
        {"type": "way", "id": 2, "tags": {"highway": "primary"},
         "geometry": [{"lat": 31.2, "lon": 121.5}, {"lat": 31.21, "lon": 121.51}]},
        {"type": "way", "id": 3, "tags": {"building": "yes"},
         "geometry": [
             {"lat": 31.2, "lon": 121.5}, {"lat": 31.2, "lon": 121.51},
             {"lat": 31.21, "lon": 121.51}, {"lat": 31.21, "lon": 121.5},
         ]},
    ]}
    layers = classify(payload)
    assert {name: len(rows) for name, rows in layers.items()} == {
        "buildings": 1, "roads": 1, "pois": 1,
    }
    assert layers["buildings"][0][3]["coordinates"][0][0] == \
        layers["buildings"][0][3]["coordinates"][0][-1]
