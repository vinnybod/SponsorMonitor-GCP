import configparser
from typing import Dict
from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


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
        tiers={k: v for k, v in config["Tiers"].items()},
    )
