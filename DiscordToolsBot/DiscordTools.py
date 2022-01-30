import os
import traceback

import config
import discord
from discord.ext import commands

from pathlib import Path

bot = commands.Bot(
    description="Tools Discord Bot",
    activity=discord.Game("Trabalhando..."),
    help_command=None,
    command_prefix=config.PREFIX,
    case_insensitive=True,
    strip_after_prefix=True,
)


@bot.event
async def on_ready():
    print(f"{bot.user.name} tá on")

if __name__ == "__main__":
    for extension in os.listdir(Path(__file__).parent/"cogs/"):
        if extension.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{extension[:-3]}")
            except Exception:
                print(f"{extension} couldn't be loaded.")
                traceback.print_exc()
                print("")

bot.run(config.TOKEN)