import os
from discord.ext import commands

from bot.bot import Bot

os.chdir("./")

disc_bot = Bot()
disc_bot.initialize()