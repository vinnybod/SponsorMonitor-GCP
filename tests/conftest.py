import logging
import pytest
import json


@pytest.fixture
def new_sponsor_payload():
    with open("tests/new_sponsor.json") as payload:
        return json.load(payload)


@pytest.fixture
def sponsor_tier_change_payload():
    with open("tests/sponsor_tier_change.json") as payload:
        return json.load(payload)
