import discord
from discord.ext import commands

from constants import verified_role, stage_1_role, stage_2_role, stage_3_role, alumni_role
from utils import is_committee_member
from views import confirm
from bot.bot import Bot

class CommitteeCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(name="verify", description="For committee members to verify a student.")
    async def verify(self, ctx: commands.Context, user: discord.Member):
        if not is_committee_member(ctx):
            print(f"User {ctx.author} attempted to use verify command without permission.")
            await ctx.send("You do not have permission to use this command.")
            return
        verified = ctx.guild.get_role(verified_role)  # type: ignore
        if verified is None:
            await ctx.send("Verified role not found in this server.", ephemeral=True)
            return
        await user.add_roles(verified)
        await ctx.send(f"{user.mention} has been verified.")

    @commands.hybrid_command(name="unverify", description="For committee members to unverify a student.")
    async def unverify(self, ctx: commands.Context, user: discord.Member):
        if not is_committee_member(ctx):
            print(f"User {ctx.author} attempted to use unverify command without permission.")
            await ctx.send("You do not have permission to use this command.")
            return
        verified = ctx.guild.get_role(verified_role)  # type: ignore
        if verified is None:
            await ctx.send("Verified role not found in this server.", ephemeral=True)
            return
        await user.remove_roles(verified)
        await ctx.send(f"{user.mention} has been unverified.")

    @commands.hybrid_command(name="unverify_all", description="For committee members to unverify all students.")
    async def unverify_all(self, ctx: commands.Context):
        if not is_committee_member(ctx):
            print(f"User {ctx.author} attempted to use unverify_all command without permission.")
            await ctx.send("You do not have permission to use this command.")
            return
        await ctx.send("Please take extreme caution when running this command. This command removes verification from all users in the server.")
        if not await confirm(ctx):
            return
        await ctx.send("Are you absolutely sure you want to UNVERIFY ALL USERS?\nThis action is not reversable without a few hours of work, blood, sweat, and tears.\nPlease make sure you are running the right command.\nYou are about to remove the 'Verified' role from everyone in the server.")
        if not await confirm(ctx):
            return
        await ctx.send("Okay. Unverifying all users now. This may take a few minutes.")
        verified = ctx.guild.get_role(verified_role)  # type: ignore
        if verified is None:
            await ctx.send("Verified role not found in this server.", ephemeral=True)
            return
        for member in ctx.guild.members:  # type: ignore
            if verified in member.roles:
                print(f"Removing verified role from {member}.")
                await member.remove_roles(verified)
        await ctx.send("All users have been unverified.")

    @commands.hybrid_command(name="stage_up", description="Move all users in the server up a stage.")
    async def stage_up(self, ctx: commands.Context):
        if not is_committee_member(ctx):
            print(f"User {ctx.author} attempted to use stage_up command without permission.")
            await ctx.send("You do not have permission to use this command.")
            return
        if not await confirm(ctx):
            return
        await ctx.send("Moving all users up a stage now. This may take a few minutes.")
        stage_1 = ctx.guild.get_role(stage_1_role)  # type: ignore
        stage_2 = ctx.guild.get_role(stage_2_role)  # type: ignore
        stage_3 = ctx.guild.get_role(stage_3_role)  # type: ignore
        alumni = ctx.guild.get_role(alumni_role)  # type: ignore
        if stage_1 is None or stage_2 is None or stage_3 is None or alumni is None:
            await ctx.send("One or more stage roles not found in this server.", ephemeral=True)
            return
        for member in ctx.guild.members:  # type: ignore
            print(f"Editing roles for {member}.")
            if stage_1 in member.roles:
                await member.remove_roles(stage_1)
                await member.add_roles(stage_2)
            elif stage_2 in member.roles:
                await member.remove_roles(stage_2)
                await member.add_roles(stage_3)
            elif stage_3 in member.roles:
                await member.remove_roles(stage_3)
                await member.add_roles(alumni)
        await ctx.send("All users have been moved up a stage.\nPlease make an announcement to the server to inform members of this change.")

    @commands.hybrid_command(name="verify_all", description="For committee members to verify all students.")
    async def verify_all(self, ctx: commands.Context):
        """
        quite rare for this to be used, im only making this whilst locking down the server.
        this verifies EVERYONE below the nucats bot role, so be careful, youll probs verify a bot or two but easy to get rid of when they pop up.
        """
        if not is_committee_member(ctx):
            print(f"User {ctx.author} attempted to use verify_all command without permission.")
            await ctx.send("You do not have permission to use this command.")
            return
        if not await confirm(ctx):
            return
        await ctx.send("Verifying all users now. This may take a few minutes.")
        verified = ctx.guild.get_role(verified_role)  # type: ignore
        if verified is None:
            await ctx.send("Verified role not found in this server.", ephemeral=True)
            return
        for member in ctx.guild.members:  # type: ignore
            if verified not in member.roles:
                print(f"Adding verified role to {member}.")
                await member.add_roles(verified)
        await ctx.send("All users have been verified.")

async def setup(bot: Bot):
    await bot.add_cog(CommitteeCog(bot))
