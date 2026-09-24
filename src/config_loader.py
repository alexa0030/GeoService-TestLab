from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str | Path) -> dict:
    target = Path(path)
    if not target.is_absolute():
        target = ROOT / target
    with target.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    return value or {}


def load_services() -> dict:
    return load_yaml("config/services.yaml")["services"]

