import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

startup_extensions = [f"src.cogs.{x[:-3]}"
                      for x in os.listdir(os.getcwd() + "/cogs")
                      if x[-3:] == ".py"]

if __name__ == "__main__":
    # Setup env
    load_dotenv()
    DISCORD_TOKEN = os.getenv("discord_token")

    # Initial setup bot
    bonora_bot = commands.Bot(command_prefix="!")
    loaded_ext = []
    for extension in startup_extensions:
        try:
            bonora_bot.load_extension(extension)
            loaded_ext.append(extension.split(".")[-1])
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print("###################")
            print('Failed to load extension {}\n{}'.format(extension, exc))
            print("###################")


    # Run bot
    bonora_bot.run(DISCORD_TOKEN)
