import discord
import json
import os
import requests
from dotenv import load_dotenv
import random
import requests
import aiohttp

load_dotenv()

GUILD = int(os.getenv("GUILD_ID"))
TOKEN = os.getenv("DISCORD_TOKEN")
GLENTRE_STATUS_CHANNEL_ID = int(os.getenv("GLENTRE_STATUS_CHANNEL_ID"))

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hi to georbert")
async def hello(ctx):
    intro_list = [
        "omg",
        ":eyes:",
        "oh",
    ]
    greeting_list = [
        "hi",
        "hiii",
        "hiiiii",
        "hello",
        "helloo",
        "hellllooo",
        "HI!",
        "hai",
        "haii",
    ]
    exclaimation_list = [
        "!",
        "!!",
        "!!!",
    ]
    happy_emoji_list = [
        ":wave:",
        ":3",
        "^_^",
        ":flushed:",
        "<:Cool_Blush:956281399797772399>",
        "<:headpats:1023403755682660454>",
        "<:imgay:991802607309955123>",
        "<:mreorw:963655891029229609>",
        "<:ohheheimthecutest:961069609413378108>",
        "<:ohurmyoureyeslookdelish:984622629069660201>",
        "<:pepegay:991802609616818377>",
        "<:pog:1021113025106825257>",
        ":bangbang:",
        ":point_right::point_left:",
    ]

    default_str = ""

    # string has a 30% chance to start with a keysmash
    if random.randint(1, 100) < 30:
        for i in range(random.randint(3, 5)):
            # string is consonants weighted to include more of the middle keys
            default_str += random.choice("sdfjk")
        for i in range(random.randint(5, 10)):
            # string is consonants weighted to include more of the middle keys
            default_str += random.choice("bcdfghjklmnpqrstvwxzasdfghjkli;")

    # string has a 30% chance to have an extra intro
    if random.randint(1, 100) < 30:
        default_str = random.choice(intro_list)

    # string has a 50% chance to have 2 greetings
    if random.randint(1, 100) < 50:
        default_str += " " + random.choice(greeting_list)

    # random greeting + exclaimation
    default_str += " " + (
        random.choice(greeting_list) + random.choice(exclaimation_list)
    )

    # place emoji either at beginning or end of string
    if random.randint(1, 100) < 50:
        default_str += " " + random.choice(happy_emoji_list)
    else:
        default_str = random.choice(happy_emoji_list) + " " + default_str

    # flavor text
    response_scheme = random.choices(list(range(4)), weights=(2, 0.5, 1, 2), k=1)[0]
    if response_scheme == 0:
        # default
        quip = [
            "Nice to meet you!",
            "How are things?",
            "What's new?",
            "What's up?",
            "You look awesome today!",
            "Have a nice day!",
            "I hope you're doing well!",
            "Good to see you!",
            "How are you doing?",
            "My name is Georbert!",
            "Remember to drink water!",
            "Check your posture!",
            "Take a break from your screen every now and then!",
            "\nIn case you didn't know, the glow center is located in the 3rd floor SLC! Come say hi!",
        ]
        await ctx.respond(default_str + " " + random.choice(quip))

    elif response_scheme == 1:
        # fun fact
        session = aiohttp.ClientSession()
        response = await session.get(
            "https://uselessfacts.jsph.pl/random.json?language=en"
        )
        responsej = await response.json()
        await session.close()

        # clean up the string
        response_text = responsej["text"]
        response_text = (
            response_text[0].lower() + response_text[1:-1]
        )  # remove first letter capitalization and the final period
        if random.choice([0, 1]) == 1:
            response_text = "\nDid you know that " + response_text + "?"
        else:
            response_text = "\nFun fact: " + response_text + "!"

        await ctx.respond(default_str + response_text)

    elif response_scheme == 2:
        # open status
        if "closed" in bot.get_channel(GLENTRE_STATUS_CHANNEL_ID).name:
            await ctx.respond(default_str + " the glentre is currently closed!")
        else:
            await ctx.respond(default_str + " the glentre is currently open!")

    elif response_scheme == 3:
        # activity suggestion
        session = aiohttp.ClientSession()
        response = await session.get("https://www.boredapi.com/api/activity/")
        responsej = await response.json()
        await session.close()

        # clean up the string
        response_text = responsej["activity"]
        response_text = (
            response_text[0].lower() + response_text[1:]
        )  # remove first letter capitalization

        formats = [
            "\nYou should {0} today!",
            "\nIf you have time, {0}!",
            "\nIf you're bored, you should {0}!",
            "\nYou can always {0} if you're bored!",
            "\nYou might want to {0}!",
            "\nRemember to {0}!",
            "\nDo you want to {0} with me?",
            "\nWe should {0} together!",
            "\nWe should {0} together... Haha jk... Unless? :flushed:",
            "\nYou. Me. {0}. Now.",
            "\nBe honest. You always wanted to {0}.",
            "\nI know your deepest desires. It is to {0}.",
            "\nMr. Goose says: {0}!",
        ]

        await ctx.respond(default_str + random.choice(formats).format(response_text))


@bot.slash_command(
    name="glentre-status", description="Change the glentre status from closed/open."
)
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


@bot.slash_command(name="eepy", description="For when you're feeling a bit eepy.")
async def eepy(ctx):
    await ctx.respond(
        "https://media.tenor.com/izCcDz-s6XoAAAAC/eepy-and-why-he-eepy.gif"
    )


@bot.slash_command(name="zawarudo", description="Weeb.")
async def stand(ctx):
    await ctx.respond(
        "https://media.discordapp.net/attachments/1020012959369531503/1032745623432208485/Untitled_Artwork.png?width=439&height=754"
    )


bot.run(TOKEN)
