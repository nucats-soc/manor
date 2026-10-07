import discord, os, asyncio
from discord.ext import commands

from utils.utils import color_message
from constants import TOKEN

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", 
                         intents=intents, 
                         help_command=None, 
                         allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=False), 
                         allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=False, private_channel=False))
        self.unloaded_cogs = []

    def initialize(self):
        os.system("cls")
        print(color_message(message="Initializing bot...", color="yellow"))
        asyncio.run(self.load_extensions())
        self.run(TOKEN) # type: ignore

    async def load_extensions(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(color_message(message=f"Loaded extension {filename}", color="green"))
                except Exception as e:
                    print(e)
                    print(color_message(message=f"Failed to load extension {filename}", color="red"))
                    self.unloaded_cogs.append(filename.capitalize()[-3])

    async def on_ready(self):
        print(color_message(message=f"Logged in as {self.user}!", color="green"))
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"Prefix: !"))
                