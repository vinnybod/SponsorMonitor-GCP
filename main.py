import asyncio
import logging

from pydantic import ValidationError

from sponsormonitor import github
from sponsormonitor import config
from sponsormonitor.models import SponsorAction, SponsorActivity, PingPayload
from flask import make_response

log = logging.getLogger("sponsormonitor")

settings = config.get_settings()


def sponsormonitor(request):
    return asyncio.run(do_work(request))


async def do_work(request):
    data = None
    try:
        data = SponsorActivity.parse_obj(request.get_json())
    except ValidationError as e:
        log.info("Could not parse to sponsoractivity")
    try:
        data = PingPayload.parse_obj(request.get_json())
    except ValidationError as e:
        log.info("Could not parse to pingpayload")

    if data is None:
        return make_response({'error': 'could not parse payload'}, 400)

    if not request.headers.get("X-Hub-Signature"):
        return make_response({'error': 'no signature'}, 400)

    if not await github.verify_signature(
            request.data, request.headers["X-Hub-Signature"]
    ):
        return make_response({'error': 'signature not verified'}, 400)

    if isinstance(data, PingPayload):
        log.info("Received ping payload, webhook successfully configured")
        return make_response({}, 200)

    log.info(f"Sponsorship update: {data.action}")

    user = data.sponsorship["sponsor"]["login"]
    user_id = data.sponsorship["sponsor"]["id"]
    tier = int(data.sponsorship["tier"]["monthly_price_in_dollars"])

    if data.action == SponsorAction.CREATED:
        await github.send_org_invite(user_id, tier)

    elif data.action == SponsorAction.CANCELLED:
        await github.remove_user_from_org(user)

    elif data.action == SponsorAction.PENDING_TIER_CHANGE:
        from_tier = data.changes["tier"]["from"]["monthly_price_in_dollars"]

        if tier < settings.minimum_tier:
            await github.remove_user_from_org(user)
        elif tier >= settings.minimum_tier and from_tier < settings.minimum_tier:
            await github.send_org_invite(user_id, tier)

    return make_response({}, 200)
