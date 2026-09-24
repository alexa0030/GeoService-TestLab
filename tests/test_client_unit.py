from unittest.mock import Mock

import requests

from src.api_client import ServiceConfig, TileClient, service_config


def make_client():
    session = Mock()
    config = ServiceConfig("demo", "http://localhost:9999/", "/layer/{z}/{x}/{y}", "/catalog")
    return TileClient(config, timeout=3, session=session), session


def test_tile_url_is_formatted():
    client, session = make_client()
    session.get.return_value.status_code = 200
    client.get_tile(6, 52, 26)
    session.get.assert_called_once_with("http://localhost:9999/layer/6/52/26", timeout=3)


def test_catalog_url_is_formatted():
    client, session = make_client()
    client.get_catalog()
    session.get.assert_called_once_with("http://localhost:9999/catalog", timeout=3)


def test_layer_can_be_replaced():
    client, session = make_client()
    client.config = ServiceConfig("demo", "http://host", "/public.sample_features/{z}/{x}/{y}", "/catalog")
    client.get_layer("missing", 1, 1, 1)
    session.get.assert_called_once_with("http://host/missing/1/1/1", timeout=3)


def test_wait_until_ready_succeeds_without_sleep():
    client, session = make_client()
    session.get.return_value.status_code = 200
    assert client.wait_until_ready(attempts=1, delay=0)


def test_wait_until_ready_returns_false():
    client, session = make_client()
    session.get.side_effect = requests.RequestException("offline")
    assert client.wait_until_ready(attempts=1, delay=0) is False


def test_service_config_factory():
    cfg = service_config("demo", {"base_url": "http://x", "tile_path": "/t/{z}/{x}/{y}", "catalog_path": "/c"})
    assert cfg.name == "demo"
