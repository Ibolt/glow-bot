import discord
import os
from dotenv import load_dotenv

load_dotenv()

GUILD = int(os.getenv("GUILD_ID"))
TOKEN = os.getenv("DISCORD_TOKEN")
GLENTRE_STATUS_CHANNEL_ID = int(os.getenv("GLENTRE_STATUS_CHANNEL_ID"))

bot = discord.Bot(debug_guilds=[GUILD])


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name = "hello", description = "Say hi to georbert")
async def hello(ctx):
    await ctx.respond("hi <:ohheheimthecutest:961069609413378108>")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id != GLENTRE_STATUS_CHANNEL_ID:
        return

    prefix = "glentre-"
    if "closed" in message.channel.name:
        status = "open ✅"
    else:
        status = "closed ❌"
    
    await message.channel.send(f"The Glentre is now {status}!")
    await message.channel.edit(name=prefix + status)

bot.run(TOKEN)
