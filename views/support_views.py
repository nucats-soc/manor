import discord, asyncio, io, time
from chat_exporter import chat_exporter

from bot.bot import Bot
from db import get_db, OpenTickets
from constants import TICKET_CATEGORY_ID, committee_role, COLOUR_MAIN, COLOUR_NEUTRAL, COLOUR_GOOD, ticket_log_channel

creation_cooldown = []

class Ticket_Open(discord.ui.View):
    def __init__(self, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="nucats:open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in creation_cooldown:
            await interaction.response.send_message("You are on cooldown for creating tickets. Please wait a few minutes before trying again.", ephemeral=True)
            return

        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        creation_cooldown.append(interaction.user.id)

        while not self.bot.is_ready():
            await asyncio.sleep(1)

        with get_db() as db:
            existing_ticket = db.query(OpenTickets).filter_by(user_id=interaction.user.id).first()
            if existing_ticket:
                existing_channel = self.bot.get_channel(existing_ticket.channel_id) # type: ignore
                if existing_channel:
                    await existing_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, view_channel=True, embed_links=True, attach_files=True) # type: ignore
                    await interaction.followup.send(f"You already have an open ticket, use that one instead.\n\n{existing_channel.mention}", ephemeral=True) # type: ignore
                    creation_cooldown.remove(interaction.user.id)
                    return
                else:
                    db.delete(existing_ticket)
                    db.commit()

        if interaction.guild is None:
            await interaction.followup.send("This command can only be used in a server.", ephemeral=True)
            creation_cooldown.remove(interaction.user.id)
            return


        category = interaction.guild.get_channel(TICKET_CATEGORY_ID)
        if not isinstance(category, discord.CategoryChannel):
            category = None

        committee = interaction.guild.get_role(committee_role)
        if committee is None:
            await interaction.followup.send("The committee role does not exist in this server. Please contact an administrator.", ephemeral=True)
            creation_cooldown.remove(interaction.user.id)
            return

        ticket = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            topic=f"Ticket for {interaction.user.name} ({interaction.user.id})",
            overwrites={
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, manage_channels=True, manage_messages=True, send_messages=True, embed_links=True, attach_files=True),
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                committee: discord.PermissionOverwrite(read_messages=True, send_messages=True, embed_links=True, attach_files=True),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, embed_links=True, attach_files=True)
            }
        )

        embed = discord.Embed(title="Ticket Created", description=f"Your ticket has been created. Please wait for a committee member to assist you.", color=discord.Colour.blue())
        msg = await ticket.send(content=f"{interaction.user.mention}{committee.mention}", embed=embed, view=Ticket_Close(self.bot))
        await msg.pin()

        with get_db() as db:
            new_ticket = OpenTickets(user_id=interaction.user.id, channel_id=ticket.id)
            db.add(new_ticket)
            db.commit()

        creation_cooldown.remove(interaction.user.id)

        await interaction.followup.send(f"Your ticket has been created: {ticket.mention}", ephemeral=True)

class Ticket_Close(discord.ui.View):
    def __init__(self, bot: Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="nucats:close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("This button can only be used in a server.", ephemeral=True)
            return

        assert interaction.guild is not None, "Interaction guild is None"
        assert interaction.channel is not None, "Interaction channel is None"
        assert interaction.message is not None, "Interaction message is None"

        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("This button can only be used in a text channel.", ephemeral=True)
            return

        with get_db() as db:
            ticket = db.query(OpenTickets).filter_by(channel_id=interaction.channel.id).first()
            if not ticket:
                await interaction.response.send_message("This channel is not a ticket.", ephemeral=True)
                return

        await interaction.message.edit(view=None)

        embed = discord.Embed(title="Ticket Closing log", colour=COLOUR_MAIN)
        await interaction.channel.send(embed=embed)
        embed = discord.Embed(title="Removing ticket from database", colour=COLOUR_NEUTRAL)
        msg = await interaction.channel.send(embed=embed)
        with get_db() as db:
            ticket = db.query(OpenTickets).filter_by(channel_id=interaction.channel.id).first()
            ownerid: int = ticket.user_id if ticket else None # type: ignore
            if ticket:
                db.delete(ticket)
                db.commit()

        embed = discord.Embed(title="Removed ticket from database", colour=COLOUR_GOOD)
        await msg.edit(embed=embed)
        embed = discord.Embed(title="Generating transcript", colour=COLOUR_NEUTRAL)
        msg = await interaction.channel.send(embed=embed)

        transcript = await chat_exporter.export(interaction.channel, 
                                                limit=None,
                                                tz_info="UTC",
                                                guild=interaction.guild,
                                                military_time=True,
                                                fancy_times=False,
                                                bot=self.bot)
        if transcript is None:
            embed = discord.Embed(title="Failed to generate transcript", colour=discord.Colour.red())
            await msg.edit(embed=embed)
            return

        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{interaction.channel.name}.html",
        )

        log_embed = discord.Embed(title="Ticket closed", description=f"""Ticket: {interaction.channel.name} ({interaction.channel.id})\nClosed By: {interaction.user.mention} ({interaction.user.id})\nCreated By: <@{ownerid}> ({ownerid})""", colour=COLOUR_MAIN)
        log_channel = interaction.guild.get_channel(ticket_log_channel)
        if log_channel is not None and isinstance(log_channel, discord.TextChannel):
            await log_channel.send(embed=log_embed, file=transcript_file)
            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{interaction.channel.name}.html",
            )
        try:
            if ownerid:
                member = interaction.guild.get_member(int(ownerid))
                if member:
                    member_embed=discord.Embed(title="Ticket closed", description=f"Your ticket has been closed. The transcript is attached above", colour=COLOUR_MAIN)
                    await member.send(embed=member_embed, file=transcript_file)
        except Exception as e:
            print(e)
            pass

        embed = discord.Embed(title="Transcript Generated", colour=COLOUR_GOOD)
        await msg.edit(embed=embed)
        await interaction.channel.send(embed=discord.Embed(title="", description=f"This channel will be deleted <t:{round(time.time())+11}:R>", colour=COLOUR_NEUTRAL))
        await asyncio.sleep(10)
        await interaction.channel.delete()


async def reset_cooldown_loop():
    global creation_cooldown
    creation_cooldown = []