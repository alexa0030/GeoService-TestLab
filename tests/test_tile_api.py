import pytest


@pytest.mark.integration
@pytest.mark.parametrize("z,x,y", [(0, 0, 0), (6, 53, 26), (10, 857, 418)])
def test_valid_tile_response(client, z, x, y):
    response = client.get_tile(z, x, y)
    assert response.status_code == 200
    assert response.headers["content-type"].split(";")[0] in {
        "application/vnd.mapbox-vector-tile",
        "application/x-protobuf",
        "application/octet-stream",
    }


@pytest.mark.integration
def test_tile_request_is_binary(client):
    response = client.get_tile(6, 53, 26)
    assert isinstance(response.content, bytes)
