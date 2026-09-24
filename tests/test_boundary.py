import pytest


@pytest.mark.integration
@pytest.mark.parametrize("z,x,y", [(-1, 0, 0), (23, 0, 0), (6, -1, 26)])
def test_invalid_coordinates_are_rejected(client, z, x, y):
    assert client.get_tile(z, x, y).status_code in {400, 404, 422, 500}

