from __future__ import annotations

import time
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class ServiceConfig:
    name: str
    base_url: str
    tile_path: str
    catalog_path: str


class TileClient:
    def __init__(self, config: ServiceConfig, timeout: float = 10, session=None):
        self.config = config
        self.timeout = timeout
        self.session = session or requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get_catalog(self):
        return self.session.get(self._url(self.config.catalog_path), timeout=self.timeout)

    def get_tile(self, z: int, x: int, y: int):
        path = self.config.tile_path.format(z=z, x=x, y=y)
        return self.session.get(self._url(path), timeout=self.timeout)

    def get_layer(self, layer: str, z: int = 0, x: int = 0, y: int = 0):
        path = self.config.tile_path.replace("public.sample_features", layer)
        path = path.replace("sample_features", layer)
        return self.session.get(self._url(path.format(z=z, x=x, y=y)), timeout=self.timeout)

    def wait_until_ready(self, attempts: int = 10, delay: float = 2) -> bool:
        for index in range(attempts):
            try:
                if self.get_catalog().status_code == 200:
                    return True
            except requests.RequestException:
                pass
            if index < attempts - 1:
                time.sleep(delay)
        return False


def service_config(name: str, raw: dict) -> ServiceConfig:
    return ServiceConfig(name=name, **raw)
