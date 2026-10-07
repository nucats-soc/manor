import random
import discord
from discord.ext import commands

from constants import welcome_channel
from utils import random_status_code


class MemberEventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(welcome_channel)
        await channel.send(f"Welcome {member.mention} to the NUCATS Discord server! Please read the rules and verify yourself using the authentication button in the auth channel.")  # type: ignore
        await channel.send(f"https://http.cat/{random_status_code()}")  # type: ignore

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberEventsCog(bot))
