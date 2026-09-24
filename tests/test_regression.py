import pytest


@pytest.mark.integration
@pytest.mark.regression
def test_repeated_core_request_is_stable(client):
    responses = [client.get_tile(6, 53, 26) for _ in range(3)]
    assert {response.status_code for response in responses} == {200}
    assert len({response.content for response in responses}) == 1


@pytest.mark.integration
@pytest.mark.regression
def test_both_services_publish_expected_layer(client):
    body = client.get_catalog().text
    assert "sample_features" in body
