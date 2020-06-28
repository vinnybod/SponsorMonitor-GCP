import pytest
from sponsormonitor import config


def test_get_settings():
    settings = config.get_settings()
    assert settings.minimum_tier == 15
    assert settings.github_org == "Porchetta-Industries"
    assert settings.tiers == {
        6: "Supporter",
        15: "Sponsors",
        30: "Sponsors",
        100: "Freelance Sponsors",
        300: "Gold Sponsors",
    }
