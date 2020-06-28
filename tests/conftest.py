import logging
import pytest
import json
import hmac
import os

log = logging.getLogger("sponsormonitor")
log.setLevel(logging.DEBUG)

def get_hub_sig_digest(json_file):
    secret = os.getenv("SECRET_TOKEN").encode()
    with open(json_file, "rb") as raw:
        digest = hmac.new(secret, raw.read(), digestmod="sha1").hexdigest()
        return f"sha1={digest}"


def get_json_with_hub_signature(json_file):
    with open(json_file) as payload:
        return get_hub_sig_digest(json_file), json.load(payload)


def get_data_with_hub_signature(json_file):
    with open(json_file, "rb") as raw:
        data = raw.read()
        return get_hub_sig_digest(json_file), data


def get_json(json_file):
    with open(json_file) as payload:
        return json.load(payload)


@pytest.fixture
def raw_new_sponsor_payload_with_sig():
    return get_data_with_hub_signature("tests/new_sponsor.json")


@pytest.fixture
def raw_sponsor_tier_change_payload_with_sig():
    return get_data_with_hub_signature("tests/sponsor_tier_change.json")


@pytest.fixture
def raw_ping_payload_with_sig():
    return get_data_with_hub_signature("tests/ping.json")


@pytest.fixture
def new_sponsor_payload_with_sig():
    return get_json_with_hub_signature("tests/new_sponsor.json")


@pytest.fixture
def sponsor_tier_change_payload_with_sig():
    return get_json_with_hub_signature("tests/sponsor_tier_change.json")


@pytest.fixture
def ping_payload_with_sig():
    return get_json_with_hub_signature("tests/ping.json")


@pytest.fixture
def new_sponsor_payload():
    return get_json("tests/new_sponsor.json")


@pytest.fixture
def sponsor_tier_change_payload():
    return get_json("tests/sponsor_tier_change.json")


@pytest.fixture
def ping_payload():
    return get_json("tests/ping.json")
