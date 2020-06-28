import pytest
import asyncio
from sponsormonitor import github


@pytest.mark.asyncio
async def test_verify_signature(raw_new_sponsor_payload_with_sig):
    sig, raw_payload = raw_new_sponsor_payload_with_sig
    assert await github.verify_signature(raw_payload, sig) == True
