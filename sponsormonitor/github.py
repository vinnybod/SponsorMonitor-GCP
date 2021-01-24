import asyncio
import httpx
import logging
import hmac
import hashlib
from sponsormonitor import config

log = logging.getLogger("sponsormonitor.github")

settings = config.get_settings()


# https://docs.github.com/en/rest/reference/teams#list-teams
async def get_team_slug(team_name):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://api.github.com/orgs/{settings.github_org}/teams",
            headers={"Authorization": f"token {settings.github_access_token}"},
        )

        teams = list(filter(lambda t: t["name"].lower() == team_name.lower(), r.json()))

        if not r.status_code == 200:
            raise Exception(f"Unexpected status code returned {r.status_code}: {r.text}")

        if len(teams) == 1:
            return teams[0]["slug"]

        raise Exception(f"Unexpected number of teams returned: {len(teams)}")


# https://docs.github.com/en/rest/reference/teams#add-or-update-team-membership-for-a-user
async def send_org_invite(user: str, tier: int):
    team_name = settings.tiers.get(tier)
    if not team_name:
        raise Exception(
            f"Tier doesn't seemed to be defined in config. Received tier: {tier}"
        )

    team_slug = await get_team_slug(team_name)

    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"https://api.github.com/orgs/{settings.github_org}/teams/{team_slug}/memberships/{user}",
            headers={"Authorization": f"token {settings.github_access_token}"},
            json={"role": "member"},
        )

        if not r.status_code == 200:
            raise Exception(f"Unexpected status code returned {r.status_code}: {r.text}")


# https://docs.github.com/en/rest/reference/orgs#remove-an-organization-member
async def remove_user_from_org(user):
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"https://api.github.com/orgs/{settings.github_org}/memberships/{user}",
            headers={"Authorization": f"token {settings.github_access_token}"},
        )

        if not r.status_code == 204:
            raise Exception(f"Unexpected status code returned {r.status_code}: {r.text}")


# https://developer.github.com/webhooks/securing/
async def verify_signature(request_body: bytes, signature_header: str) -> bool:
    digest = hmac.new(settings.secret_token.encode(), request_body, "sha1").hexdigest()
    return hmac.compare_digest(f"sha1={digest}", signature_header)
