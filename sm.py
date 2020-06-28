import asyncio
import logging
from typing import Union
from sponsormonitor import github
from sponsormonitor import config
from sponsormonitor.models import SponsorAction, SponsorActivity, PingPayload
from fastapi import FastAPI, Depends
from fastapi import Response, status, Request

app = FastAPI()
log = logging.getLogger("sponsormonitor")


@app.post("/")
async def handle_sponsor_webhook(
    data: Union[SponsorActivity, PingPayload],
    request: Request,
    settings: config.Settings = Depends(config.get_settings),
):
    if not request.headers.get("X-Hub-Signature"):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    if not await github.verify_signature(
        await request.body(), request.headers["X-Hub-Signature"]
    ):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    if isinstance(data, PingPayload):
        log.info("Received ping payload, webhook successfully configured")
        return Response(status_code=status.HTTP_200_OK)

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

    return Response(status_code=status.HTTP_200_OK)
