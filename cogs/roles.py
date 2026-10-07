import discord
from discord.ext import commands

from bot import Bot
from constants import committee_role
from utils import color_message
from views.role_views import RolePanel


class RolesCog(commands.Cog):
	def __init__(self, bot: Bot):
		self.bot = bot

	@commands.hybrid_command(name="role_panel", description="Post the role panel in a specified channel.")
	async def role_panel(self, ctx: commands.Context, channel: discord.TextChannel):
		if not isinstance(ctx.author, discord.Member) or committee_role not in [
			role.id for role in ctx.author.roles
		]:
			await ctx.send("You do not have permission to use this command.", ephemeral=True)
			return

		embed = discord.Embed(
			title="Choose your roles",
			description=(
				"Use the menus below to manage your optional roles.\n\n"
				"**Pronouns, stage, and colour:** choose one.\n"
				"**Announcements:** select roles to toggle them on or off."
			),
			color=discord.Colour.blurple(),
		)
		await channel.send(embed=embed, view=RolePanel())
		await ctx.send("Role panel sent.", ephemeral=True)

	@commands.Cog.listener()
	async def on_ready(self):
		try:
			self.bot.add_view(RolePanel())
			print(color_message("Loaded RolePanel view", color="green"))
		except (discord.ClientException, ValueError) as error:
			print(error)
			print(color_message("Failed to load RolePanel view", color="red"))


async def setup(bot: Bot):
	await bot.add_cog(RolesCog(bot))