# SponsorMonitor

This is a simple service which monitors Github sponsors (via the built-in sponsor webhook functionality) and automatically adds them to a specific Github Organization team depending on the sponsorship tier.

# Motivation

This was built to encourage OSS developers (specifically Infosec tool developers) to adopt the [Sponsorware](https://github.com/sponsorware/docs) release model as I think it's vastly superior to the traditional commercial software model since it benefits both the OSS/Infosec community and the developer.

One of the first major problems you'll encounter if you do go down this road (and that I encountered as well) is how to actually set things up within Github to do this in a way that makes sense and doesn't drive you crazy. I'm definitely *not* saying this is the best way, but this is what I came up with and what works for me.

Since setting up SponsorMonitor requires you to go through all the steps necessary to get a working [Sponsorware](https://github.com/sponsorware/docs) setup going within Github, we're killing 2 birds with one stone: after you finish setting SponsorMonitor up, you'll have everything you need to get started releasing software under this model and as bonus points you'll have automated the process of adding your sponsors to their appropriate Github Organization team.

# Table of Contents

- [SponsorMonitor](#sponsormonitor)
  * [Motivation](#motivation)
  * [Prerequisites](#prerequisites)
  * [Workflow](#workflow)
  * [Setting up the Github Organization](#setting-up-the-github-organization)
  * [Setting up SponsorMonitor](#setting-up-sponsormonitor)
    + [Creating a Github Access Token](#creating-a-github-access-token)
    + [Creating the Webhook](#creating-the-webhook)
    + [Installing and Running SponsorMonitor](#installing-and-running-sponsormonitor)
  * [Conclusion](#conclusion)

## Prerequisites

For the setup I came up with you'll need:
- A Github user account
- A Github organization
- A VPS which SponsorMonitor will reside on (I'm using a t2.small instance on AWS EC2)
- A domain pointing to your VPS
- A valid SSL cert (Installing SponsorMonitor via Docker automates this for you)

## Workflow

The basic idea is this: you'll have a Github User account which is where people will sign up to sponsor you (it could also be a Github Organization), you'll also have specific sponsorship tiers which grant certain perks ([see mine for an example](https://github.com/sponsors/byt3bl33d3r#sponsors)). One of these tiers will be the minimum tier which will grant access to the Sponsorware (the software you only release to your sponsors, at least initially).

In order to grant access to said software in a way which makes sense, you'll need to create a Github organization as its the only way to "fine-tune" what users have access too and with what permissions. In this Github Organization, they'll be a separate team for each sponsorship tier so every time you get a new sponsor you'll have to add them to their appropriate team. This gets tedious real fast and is exactly what SponsorMonitor automates.


## Setting up the Github Organization

So to recap, you'll have one team per sponsorship tier (I've redacted the member avatars to preserve the privacy of private sponsors):

![](https://user-images.githubusercontent.com/5151193/85959543-7562ac80-b973-11ea-9cf1-c39868843015.png)

By default, all members/teams of an organization have read and write access to all the repositories in an organization. You obviously do **not** want this, so we need to change that. Go to the organization settings and do the following:

![](https://user-images.githubusercontent.com/5151193/85959814-13a34200-b975-11ea-9e41-52febc0878df.png)


Remember to also un-check the "Allow-members to create Teams" option at the bottom of the same page:

![](https://user-images.githubusercontent.com/5151193/85960009-7c3eee80-b976-11ea-9bc6-886f7257a627.png)

It's important to understand what the "*Base Permission*" setting does. Setting it to *read* will allow all members to see every repository (public or private), make comments, create PRs, create Issues etc...

Setting it to *None* will disable all of the above and you'll have go into the settings of each repository to grant read access to each team manually. I personally prefer it this way but this comes down to personal preference.

Every time I want my sponsors to see/interact with a repository I just add the teams with Read permissions under the repo's settings:

![](https://user-images.githubusercontent.com/5151193/85959948-0a66a500-b976-11ea-92f0-c0d941e26b77.png)

## Setting up SponsorMonitor

So now you have a Github user account which is where people will sign up to sponsor you, and a Github Organization where you'll invite your sponsors too in order to access your sponsorware according to their sponsorhip tier.

Problem is, you have to do this manually for each sponsor you get. every. single. time.

Additionally, if someone stops sponsoring you or changes sponsorship tier you're going to want either put them in the appropriate team or remove them from the organization. This also has to be done manually every single time.

Luckily, this is exactly what SponsorMonitor automates!

## Creating a Github Access Token

In order for SponsorMonitor to invite/remove members from/to an Organization team for you, it needs a Github Access Token (with appropriate permissions) to interact with the Github API.

To create this access token: go to the account settings of the user which created the Github Organization, click on "Developer Settings" then "Personal Access Tokens".

![](https://user-images.githubusercontent.com/5151193/85960690-e3ab6d00-b97b-11ea-8c9c-1f0e9bcc9236.png)

The only permissions needed for the access token are the *admin:org* permission. You don't need to enable anything else.

Give the Token a name and save it somewhere as it'll only be showed to you once.


## Creating the WebHook

SponsorMonitor also needs to know when you get a new sponsor, a sponsor cancels, changes tier etc... to do it's thang.

Thankfully, Github Sponsors has a webhook feature which will do an HTTP POST request with some JSON to a URL of your choosing each time some activity occurs regarding sponsorship. This is what SponsorMonitor "ingests".

To access the Webhook settings, go to your Sponsor dashboard and click on the "Webhooks" button on the left and create a new webhook.

Enter the URL pointing to the VPS where SponsorMonitor will be installed on (has to be a domain name cause TLS) and make sure the Content-Type is set to *application/json*. You're also going to want to create a secret which will be used by SponsorMonitor to validate the request is coming for Github (it'll reject anything else). I'd recommend using a strong password generated by a password manager as the secret. Plug that bad boy in to the *Secret* field and save the webhook.

![](https://user-images.githubusercontent.com/5151193/85961089-574e7980-b97e-11ea-88c7-894eeaa46115.png)

After you create it, it'll complain to you that it was unable to send the "*Ping payload*" which is normal cause we haven't set up SponsorMonitor yet.

## Installing and Running SponsorMonitor

I highly recommend using Docker/docker-compose cause it makes installing everything and setting up the Let's Encrypt TLS certificate a breeze (it'll even renew the cert for you!).

How to install docker & docker-compose is out of scope for this but just make sure you're using the latest version of both and not the ones from the OS's package manager.

Once you have a VPS going, a domain pointing to it, docker & docker-compose installed: git clone this repository and `cd` into the docker-compose folder.

There you'll see 4 files:

- `.env`: which is where you're going to be putting your Github Access Token, Wehbook Secret and Domain
- `docker-compose.yml`: the docker compose file which will set everything up (you don't have to touch this)
- `sm.conf`: the configuration file for SponsorMonitor
- `traefik.yml`: the configuration file for [Traefik](https://docs.traefik.io/) a reverse-proxy which will handle the SSL Cert creation and renewal.


### .env

Put your Github Access Token, Webhook Secret and domain pointing to your VPS in here:

```env
GITHUB_ACCESS_TOKEN=githubaccesstoken
SECRET_TOKEN=secretwebhooktoken
DOMAIN=webhook.example.com
```

### sm.conf

This is the config file for SponsorMonitor. Change this accordingly.

```conf
[Default]
# Minimum Tier that will add a user to an organization team
MinTier = 15
# Organization name
OrgName = Porchetta-Industries

[Tiers]
# This maps a specific tier to the Github Organizaton Team that the user will be added too
# e.g. 100$ sponsor tier will automatically add the user to the "Freelance Sponsors" Team
6 = Supporter
15 = Sponsors
30 = Sponsors
100 = Freelance Sponsors
300 = Gold Sponsors
```

### traefik.yml

This is the configuration for [Traefik](https://docs.traefik.io/), the only thing needed here is to change the email and comment out the `caServer` statement

```yml
# Docker configuration backend
providers:
    docker:
      defaultRule: "Host(`{{ trimPrefix `/` .Name }}.docker.localhost`)"

# API and dashboard configuration
api:
    insecure: true

entryPoints:
    web:
      address: ":80"

    websecure:
      address: ":443"

certificatesResolvers:
    myresolver:
        acme:
            email: admin@example.com # Change this to a valid email
            storage: acme.json
            caServer: "https://acme-staging-v02.api.letsencrypt.org/directory" # Staging server for testing, comment when deploying to prod
            httpChallenge:
                entryPoint: web
```

### Running SponsorMonitor

Once you got the configuration down, simply run in the same directory:

```console
docker-compose up -d
```

Congrats! Everything should be ready to go! Visit the domain and you should see that the SSL cert is valid and there's a JSON endpoint waiting for a POST request from Github!

If you want to double check everything is golden:

- Go back to the Webhook page on your Github Sponsorship Dashboard
- Under the "Recent Deliveries" section you should see the *Ping Payload" which previously failed.
- Expand the tab and hit "Redilever" 
- There now should be a green checkmark! Everything's good to go!

Now whenever you get a new sponsor they'll be added into the appropriate organization team and if they cancel or change sponsorship tiers, SponsorMonitor will change things accordingly!

## Conclusion

SponsorMonitor allows you to automate a lot of the manual tasks you'll encounter if you use a Github Organization as a way to give access to your Sponsorware.

Hopefully, this will help other people in the OSS/Infosec community to adopt the [Sponsorware](https://github.com/sponsorware/docs) model as I have and cut down on the manual tasks.

Cheers and stay safe,

M.