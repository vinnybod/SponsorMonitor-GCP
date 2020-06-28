import asyncio
import httpx
import logging
import hmac
import hashlib
from sponsormonitor import config

log = logging.getLogger("sponsormonitor.github")

settings = config.get_settings()

# https://developer.github.com/v3/teams/#list-teams
async def get_team_id(team_name):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://api.github.com/orgs/{settings.github_org}/teams",
            headers={"Authorization": f"token {settings.github_access_token}"},
        )

        teams = list(filter(lambda t: t["name"].lower() == team_name.lower(), r.json()))
        if len(teams) == 1:
            return teams[0]["id"]

        raise Exception(f"Unexpected number of teams returned: {len(teams)}")


# https://developer.github.com/v3/orgs/members/#create-an-organization-invitation
async def send_org_invite(user_id, tier):
    team_name = settings.tiers.get(tier)
    if not team_name:
        raise Exception(
            f"Tier doesn't seemed to be defined in config. Received tier: {tier}"
        )

    team_id = await get_team_id(team_name)

    invitation = {"invitee_id": 0, "role": "direct_member", "team_ids": [team_id]}

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.github.com/orgs/{settings.github_org}/invitations",
            headers={"Authorization": f"token {settings.github_access_token}"},
            json=invitation,
        )


# https://developer.github.com/v3/orgs/members/#remove-organization-membership-for-a-user
async def remove_user_from_org(user):
    async with httpx.AsyncClient() as client:
        await client.delete(
            f"https://api.github.com/orgs/{settings.github_org}/memberships/{user}",
            headers={"Authorization": f"token {settings.github_access_token}"},
        )


# https://developer.github.com/webhooks/securing/
async def verify_signature(request_body: bytes, signature_header: str) -> bool:
    digest = hmac.new(settings.secret_token.encode(), request_body, "sha1").hexdigest()
    return hmac.compare_digest(f"sha1={digest}", signature_header)
