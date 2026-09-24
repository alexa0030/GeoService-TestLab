import os

import pytest

from src.api_client import TileClient, service_config
from src.config_loader import load_services, load_yaml


@pytest.fixture(scope="session")
def services():
    return load_services()


@pytest.fixture(scope="session")
def test_config():
    return load_yaml("config/test_config.yaml")


@pytest.fixture(params=["martin", "pg_tileserv"])
def client(request, services, test_config):
    cfg = service_config(request.param, services[request.param])
    return TileClient(cfg, timeout=test_config["http"]["timeout_seconds"])


def pytest_collection_modifyitems(config, items):
    if os.getenv("RUN_INTEGRATION") == "1":
        return
    skip = pytest.mark.skip(reason="set RUN_INTEGRATION=1 with services running")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)

