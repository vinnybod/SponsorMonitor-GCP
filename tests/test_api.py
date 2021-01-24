import os
import subprocess
import uuid

import pytest
import requests
from urllib3 import Retry


# I'm a pytest noob and had issues getting this fixture to work.
# Just run the function locally on port 8080 and then run the tests :P
# @pytest.fixture(autouse=True, scope="module")
# def run_around_tests():
#     print('setting up fixture')
#     name = str(uuid.uuid4())
#     port = '8080'

#     process = subprocess.Popen(
#       [
#         'functions-framework',
#         '--target', 'sponsormonitor',
#         '--port', str(port)
#       ],
#       cwd=os.getcwd(),
#       stdout=subprocess.PIPE
#     )

#     # Send HTTP request simulating Pub/Sub message
#     # (GCF translates Pub/Sub messages to HTTP requests internally)
#     BASE_URL = f'http://localhost:{port}'

#     retry_policy = Retry(total=6, backoff_factor=1)
#     retry_adapter = requests.adapters.HTTPAdapter(
#       max_retries=retry_policy)

#     session = requests.Session()
#     session.mount(BASE_URL, retry_adapter)

#     name = str(uuid.uuid4())

#     yield
#     # res = requests.post(
#     #   BASE_URL,
#     #   json={'name': name}
#     # )
#     # assert res.text == 'Hello {}!'.format(name)

#     # Stop the functions framework process
#     print('killing fixture')
#     process.kill()
#     process.wait()


# Test receiving data without the X-Hub-Signature header
def test_recv_bad_data(raw_ping_payload_with_sig):
    _, payload = raw_ping_payload_with_sig
    r = requests.post("http://localhost:8080/", data=payload, headers={"Content-Type": "application/json"})
    assert r.status_code == 400


# Test receiving a webhook with an invalid signature
def test_recv_data_with_invalid_sig(raw_ping_payload_with_sig):
    _, payload = raw_ping_payload_with_sig

    r = requests.post(
        "http://localhost:8080/",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature": "sha1=ee02666b0187a473c90df586619a8de2ab217c2d",
        },
    )
    assert r.status_code == 400


def test_recv_ping_payload(raw_ping_payload_with_sig):
    sig, payload = raw_ping_payload_with_sig
    r = requests.post(
        "http://localhost:8080/",
        data=payload,
        headers={"Content-Type": "application/json", "X-Hub-Signature": sig},
    )
    assert r.status_code == 200

"""
def test_recv_new_sponsor(raw_new_sponsor_payload_with_sig):
    sig, payload = raw_new_sponsor_payload_with_sig
    r = requests.post(
        "http://localhost:8080/",
        data=payload,
        headers={"Content-Type": "application/json", "X-Hub-Signature": sig}
    )
    assert r.status_code == 200


def test_recv_tier_change(raw_sponsor_tier_change_payload_with_sig):
    sig, payload = raw_sponsor_tier_change_payload_with_sig

    r = requests.post(
        "http://localhost:8080/",
        data=payload,
        headers={"Content-Type": "application/json", "X-Hub-Signature": sig}
    )
    assert r.status_code == 200
"""