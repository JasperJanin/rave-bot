from LampController import lampController
from LampController import color as c
from RaveBot import raveBot

from dotenv import load_dotenv
import os
import json

import discord
from discord.commands import Option
from discord.commands.errors import ApplicationCommandInvokeError

load_dotenv()

TOKEN = os.getenv("DISCORD-BOT-TOKEN")
IP = os.getenv("BRIDGE-IP")
AUTH = os.getenv("BRIDGE-LOGIN")
GUILDS = json.loads(os.getenv("GUILDS"))

lamp = lampController.Lamp(IP, AUTH)

bot = discord.Bot()


@bot.command(guild_ids=GUILDS)
async def color(
    ctx,
    color: Option(str, "Choose a color", choices=c.colorChoices.keys())
):
    """Set Jaspers lamp color/status"""
    try:
        await lamp.setLight(c.colorChoices[color])
    except:
        pass

    message = ""
    if color == "Off":
        message = "Turned lamp off"
    else:
        message = f"Lamp set to {color}"
    await ctx.respond(message)


@bot.command(guild_ids=GUILDS)
async def rgb(
    ctx,
    r: int,
    g: int,
    b: int
):
    """Set Jaspers lamp color by RGB values"""
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    try:
        await lamp.setLight(c.rgb(r, g, b))
    except:
        pass

    message = f"Lamp set to {r}, {g}, {b}"
    await ctx.respond(message)

bot.run(TOKEN)
