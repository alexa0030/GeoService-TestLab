import pytest


@pytest.mark.integration
def test_catalog_is_available(client):
    response = client.get_catalog()
    assert response.status_code == 200
    assert response.content

