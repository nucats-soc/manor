import discord
from discord.ext import commands

async def confirm(ctx: commands.Context) -> bool:
    view = Confirm(ctx.author.id)
    message = await ctx.send("Are you sure you want to continue?", view=view, ephemeral=True)
    await view.wait()
    if view.value is None:
        await message.edit(content="Confirmation timed out.", view=None)
        return False
    if view.value:
        await message.edit(content="You have confirmed the action.", view=None)
    else:
        await message.edit(content="You have cancelled the action.", view=None)
    return view.value

class Confirm(discord.ui.View):
    def __init__(self, org_user: int=0):
        super().__init__(timeout=600)
        self.value = None
        self.org_user = org_user

    @discord.ui.button(label = "Yes", emoji = "<:Check:779247977721495573>", style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        self.clear_items()
    
    @discord.ui.button(label = "No", emoji = "<:Cross:779247977843523594>", style = discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

        self.clear_items()
    
    async def interaction_check(self, interaction: discord.Interaction):
        if self.org_user == 0:
            return True
        if interaction.user.id != self.org_user:
            await interaction.response.send_message("You can't click this!", ephemeral=True)
            return False
        
        return True

    async def on_timeout(self):
        self.stop()