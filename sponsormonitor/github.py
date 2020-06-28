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

        if not r.status_code == 200:
            raise Exception(f"Unexpected status code returned {r.status_code}: {r.text}")

        if len(teams) == 1:
            return teams[0]["id"]

        raise Exception(f"Unexpected number of teams returned: {len(teams)}")


# https://developer.github.com/v3/orgs/members/#create-an-organization-invitation
async def send_org_invite(user_id: int, tier: int):
    team_name = settings.tiers.get(tier)
    if not team_name:
        raise Exception(
            f"Tier doesn't seemed to be defined in config. Received tier: {tier}"
        )

    team_id = await get_team_id(team_name)

    invitation = {"invitee_id": user_id, "role": "direct_member", "team_ids": [team_id]}

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"https://api.github.com/orgs/{settings.github_org}/invitations",
            headers={"Authorization": f"token {settings.github_access_token}"},
            json=invitation,
        )

        if not r.status_code == 201:
            raise Exception(f"Unexpected status code returned {r.status_code}: {r.text}")


# https://developer.github.com/v3/orgs/members/#remove-organization-membership-for-a-user
async def remove_user_from_org(user):
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"https://api.github.com/orgs/{settings.github_org}/memberships/{user}",
            headers={"Authorization": f"token {settings.github_access_token}"},
        )

        if not r.status_code == 200:
            raise Exception(f"Unexpected status code returned {r.status_code}: {r.text}")


# https://developer.github.com/webhooks/securing/
async def verify_signature(request_body: bytes, signature_header: str) -> bool:
    digest = hmac.new(settings.secret_token.encode(), request_body, "sha1").hexdigest()
    return hmac.compare_digest(f"sha1={digest}", signature_header)
