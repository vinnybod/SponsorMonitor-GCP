import configparser
import pathlib
from typing import Dict, ByteString
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    github_access_token: str
    secret_token: str
    github_org: str
    tiers: Dict[int, str]
    minimum_tier: int = 15


@lru_cache()
def get_settings():
    config = configparser.ConfigParser()
    config.read(["sm.conf", "/etc/sponsormonitor/sm.conf"])
    return Settings(
        github_org=config["Default"]["OrgName"],
        minimum_tier=config["Default"]["MinTier"],
        tiers={int(k): v for k, v in config["Tiers"].items()},
    )
