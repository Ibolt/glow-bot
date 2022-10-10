import discord
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GUILD = int(os.getenv("GUILD_ID"))
TOKEN = os.getenv("DISCORD_TOKEN")
GLENTRE_STATUS_CHANNEL_ID = int(os.getenv("GLENTRE_STATUS_CHANNEL_ID"))
LAST_FM_API_KEY = os.getenv("LAST_FM_API_KEY")
LAST_FM_URL = "https://ws.audioscrobbler.com/2.0/"

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hi to georbert.")
async def hello_now(ctx):
    if ctx.author == bot.user:
        return
    await ctx.respond("hi <:ohheheimthecutest:961069609413378108>")


@bot.slash_command(name = "glentre-status", description = "Change the glentre status from closed/open.")
async def update_status(ctx):
    if ctx.channel.id != GLENTRE_STATUS_CHANNEL_ID:
        return
        
    prefix = "glentre-"
    if "closed" in ctx.channel.name:
        status = "open ✅"
    else:
        status = "closed ❌"
    
    await ctx.respond(f"The Glentre is now {status}!")
    await ctx.channel.edit(name=prefix + status)


@bot.slash_command(name = "scrobble-report", description="Get current scrobble stats for all last.fm users.")
async def gen_lastfm_auth_url(ctx):
    headers = {
        "user-agent": "Georbert"
    }
    payload = {
        "api_key": LAST_FM_API_KEY,
        "method": "user.getWeeklyTrackChart",
        "user": "infinityx_",
        "format": "json"
    }
    resp = requests.get(LAST_FM_URL, headers=headers, params=payload)
    if resp.status_code != 200:
        await ctx.respond(f"Failed to retrieve scrobbles for user.")
    else:
        scrobbles = 0
        track_chart = json.loads(resp.content)["weeklytrackchart"]
        for track in track_chart["track"]:
            scrobbles += int(track["playcount"])
        
        await ctx.respond(f"Scrobbles for past 7 days: {scrobbles}")

    print(resp)

    # auth_url = f"http://www.last.fm/api/auth/?api_key={LAST_FM_API_KEY}"
    # await ctx.respond(f"Authorize georbert to display your Last.fm stats by clicking the following link: {auth_url}")


bot.run(TOKEN)
