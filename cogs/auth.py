import discord
from discord.ext import commands

from bot.bot import Bot
from constants import committee_role
from views import AuthView
from utils import color_message


class AuthCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="auth_message", description="Post the authentication button in the auth channel.")
    async def auth_message(self, ctx: commands.Context, channel: discord.TextChannel):
        if committee_role not in [role.id for role in ctx.author.roles]: # type: ignore
            await ctx.send("You do not have permission to use this command.", ephemeral=True)
            return
        if not isinstance(channel, discord.TextChannel):
            await ctx.send("I could not find the auth channel.", ephemeral=True)
            return

        await channel.send("# Welcome to NUCATS!\nPlease click the button below to start the authentication process to prove you're a Newcastle University student.\n\nIf you are not a Newcastle University student, please create a ticket to be verified.", view=AuthView())
        await ctx.send("Authentication message posted.", ephemeral=True)


    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.bot.add_view(AuthView())
            print(color_message(message="Loaded AuthView", color="green"))
        except Exception as e:
            print(e)
            print(color_message(message="Failed to load AuthView", color="red"))


async def setup(bot: Bot):
    await bot.add_cog(AuthCog(bot))