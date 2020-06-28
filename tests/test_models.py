import pytest
from sponsormonitor.models import SponsorActivity

def test_sponsor_models(new_sponsor_payload, sponsor_tier_change_payload):
    SponsorActivity(**new_sponsor_payload)
    SponsorActivity(**sponsor_tier_change_payload)