import pytest


@pytest.mark.integration
def test_unknown_layer_is_not_found(client):
    assert client.get_layer("public.layer_does_not_exist").status_code in {400, 404}

