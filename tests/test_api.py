import pytest
from fastapi.testclient import TestClient
from sm import app

client = TestClient(app)


def test_webhook_recv(new_sponsor_payload, sponsor_tier_change_payload):
    r = client.post("/", json=new_sponsor_payload)
    print(r.json())
    assert r.status_code == 200

    r = client.post("/", json=sponsor_tier_change_payload)
    assert r.status_code == 200
