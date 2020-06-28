import asyncio
import logging
from sponsormonitor import github
from sponsormonitor import config
from sponsormonitor.models import SponsorAction, SponsorActivity
from fastapi import FastAPI, Depends
from fastapi import Response, status

app = FastAPI()
log = logging.getLogger("sponsormonitor")


@app.post("/")
async def handle_sponsor_webhook(
    data: SponsorActivity, settings: config.Settings = Depends(config.get_settings)
):
    log.info(f"Sponsorship update: {data.action}")

    user = data.sponsorship["sponsor"]["login"]
    user_id = data.sponsorship["sponsor"]["id"]
    tier = int(data.sponsorship["tier"]["monthly_price_in_dollars"])

    if data.action == SponsorAction.CREATED:
        await github.send_org_invite(user_id, tier)

    elif data.action == SponsorAction.CANCELLED:
        await github.remove_user_from_org(user)

    elif data.action == SponsorAction.PENDING_TIER_CHANGE:
        if tier < settings.minimum_tier:
            await github.remove_user_from_org(user)
        elif tier > settings.minimum_tier:
            await github.send_org_invite(user_id, tier)

    return Response(status_code=status.HTTP_200_OK)
