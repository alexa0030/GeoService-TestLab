import sys

from src.api_client import TileClient, service_config
from src.config_loader import load_services, load_yaml
from src.logger import get_logger


log = get_logger(__name__)
settings = load_yaml("config/test_config.yaml")["http"]
failed = []
for name, raw in load_services().items():
    client = TileClient(service_config(name, raw), timeout=settings["timeout_seconds"])
    if client.wait_until_ready(settings["retries"], settings["retry_delay_seconds"]):
        log.info("%s is ready", name)
    else:
        failed.append(name)
        log.error("%s did not become ready", name)
sys.exit(1 if failed else 0)

