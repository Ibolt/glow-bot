import discord
import os
from dotenv import load_dotenv

load_dotenv()

guild = int(os.getenv("GUILD_ID"))
token = os.getenv("DISCORD_TOKEN")

bot = discord.Bot(debug_guilds=[guild])

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name = "hello", description = "Say hi to georbert")
async def hello(ctx):
    await ctx.respond("hi :ohheheimthecutest:")
    if ctx.guild.members[0].nick == "new?":
        await ctx.guild.members[0].edit(nick="old!")
    else:
        await ctx.guild.members[0].edit(nick="new?")


@bot.slash_command(name = "glentre-status", description = "Toggle whether the glentre is currently open or closed.")
async def glentre_open(ctx):
    prefix = "glentre-"
    if "closed" in ctx.channel.name:
        status = "open✅"
    else:
        status = "closed❌"
    print(bot.is_ws_ratelimited())

    await ctx.channel.edit(name=prefix + status)
    await ctx.respond(f"Glentre is now {status}")

bot.run(token)
