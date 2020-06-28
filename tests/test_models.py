import pytest
from sponsormonitor.models import SponsorActivity, PingPayload


def test_sponsor_activity(new_sponsor_payload, sponsor_tier_change_payload):
    SponsorActivity(**new_sponsor_payload)
    SponsorActivity(**sponsor_tier_change_payload)

def test_ping_payload(ping_payload):
    PingPayload(**ping_payload)
