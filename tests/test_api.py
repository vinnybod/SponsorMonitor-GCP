import pytest
from fastapi.testclient import TestClient
from sm import app

client = TestClient(app)


# Test receiving data without the X-Hub-Signature header
def test_recv_bad_data(raw_ping_payload_with_sig):
    _, payload = raw_ping_payload_with_sig
    r = client.post("/", data=payload, headers={"Content-Type": "application/json"})
    assert r.status_code == 400


# Test receiving a webhook with an invalid signature
def test_recv_data_with_invalid_sig(raw_ping_payload_with_sig):
    _, payload = raw_ping_payload_with_sig

    r = client.post(
        "/",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature": "sha1=ee02666b0187a473c90df586619a8de2ab217c2d",
        },
    )
    assert r.status_code == 400


def test_recv_ping_payload(raw_ping_payload_with_sig):
    sig, payload = raw_ping_payload_with_sig
    r = client.post(
        "/",
        data=payload,
        headers={"Content-Type": "application/json", "X-Hub-Signature": sig},
    )
    assert r.status_code == 200

"""
def test_recv_new_sponsor(raw_new_sponsor_payload_with_sig):
    sig, payload = raw_new_sponsor_payload_with_sig
    r = client.post(
        "/",
        data=payload,
        headers={"Content-Type": "application/json", "X-Hub-Signature": sig,},
    )
    assert r.status_code == 200


def test_recv_tier_change(raw_sponsor_tier_change_payload_with_sig):
    sig, payload = raw_sponsor_tier_change_payload_with_sig

    r = client.post(
        "/",
        data=payload,
        headers={"Content-Type": "application/json", "X-Hub-Signature": sig,},
    )
    assert r.status_code == 200
"""