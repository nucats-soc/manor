import asyncio, datetime
import os
import random
from discord.ext import commands
from uwuipy import Uwuipy

from constants import committee_channel
from bot.bot import Bot
from utils import random_status_code


class GeneralCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.uwu = Uwuipy()

    @commands.hybrid_command(name="ping", description="Check the bot's latency.")
    async def ping(self, ctx: commands.Context):
        time = datetime.datetime.now()
        message = await ctx.send("Pong...")
        latency = (datetime.datetime.now() - time).total_seconds() * 1000
        await message.edit(content=f"Pong! Latency: {round(latency)} ms")

    @commands.hybrid_command(name="coinflip", description="Flips a coin.")
    async def coinflip(self, ctx: commands.Context):
        await ctx.send(f"Flipping coin, {ctx.author.mention}, reply with your call (heads or tails).")
        call = await self.wait_for_choice(ctx, ["heads", "tails"])
        await ctx.send(f"You called {call.title()}. Flipping the coin now...")
        await asyncio.sleep(2)
        await ctx.send(f"The coin landed on {random.choice(['Heads', 'Tails'])}.")

    @commands.hybrid_command(name="roll", description="Rolls a die.")
    async def roll(self, ctx: commands.Context, sides: int = 6, rolls: int = 1):
        if sides < 1 or rolls < 1:
            await ctx.send("Please enter a valid number of sides and rolls.")
            return
        results = [random.randint(1, sides) for _ in range(rolls)]
        await ctx.send(f"You rolled: {', '.join(map(str, results))}")

    @commands.hybrid_command(name="httpcat", description="Return a random image from http.cat.")
    async def httpcat(self, ctx: commands.Context):
        await ctx.send(f"https://http.cat/{random_status_code()}")

    @commands.hybrid_command(name="httpdog", description="Return a random image from http.dog.")
    async def httpdog(self, ctx: commands.Context):
        await ctx.send(f"https://http.dog/{random_status_code()}.jpg")

    @commands.hybrid_command(name="credits", description="Shows the credits for the bot.")
    async def credits(self, ctx: commands.Context):
        await ctx.send("```\nBot originally developed by tinyTim567\nRewritten by Jack Eilles (amnexya) with assistance from NUCATS committee.\n```")

    @commands.hybrid_command(name="urandom", description="Returns a 256-byte string pulled from /dev/urandom")
    async def urandom(self, ctx: commands.Context):
        random_hex = os.urandom(256).hex()
        await ctx.send(f"Here is your 256-byte random string, freshly baked from /dev/urandom: ```\n{random_hex}\n```\nPlease don't actually use this as a secret key, everyone here has seen it.")

    @commands.hybrid_command(name="8ball", description="A magic 8-ball that can answer anything.")
    async def eight_ball(self, ctx: commands.Context, *, question: str):
        responses = ["Probably man.", "Idk, ask me later.", "Yes.", "No.", "Maybe.", "Think of this as Microsoft Authenticator, that's how bad the outlook is.", "You are asking a computer this, so the answer is probably no.", "Yes, but only if you are a cat.", "No, but only if you are a dog.", "Yes, but only if you are a human.", "No, but only if you are a robot.", "Yes, but only if you are a fish.", "No, but only if you are a bird.", "I'm sorry, but I cannot fulfill your request. As an AI language model, I am programmed to provide helpful and informative responses, but I cannot provide answers that are inappropriate or offensive. Please ask a different question.", "Sure", "Nope", "Absolutely", "Definitely not", "I guess?", "Outlook hazy, try again later.", "Yes, in due time.", "boneless chicken", "Not sure about that one."]
        random.seed(question + str(random.randint(1, 100)))
        await ctx.send(f"{question}")
        await ctx.send(random.choice(responses))

    @commands.hybrid_command(name="bucket", description="This, is a bucket.")
    async def bucket(self, ctx: commands.Context):
        await ctx.send("https://tenor.com/view/team-fortress-2-tf2-tf2-memes-gif-12176472853573905724")

    @commands.hybrid_command(name="uwu", description="Uwuifies your text.")
    async def uwuify(self, ctx: commands.Context, text: str | None = None):
        if text is None:
            async for message in ctx.channel.history(limit=2):
                if message.author != ctx.author:
                    text = message.content
                    break
        await ctx.send(self.uwu.uwuify(text))  # type: ignore

    @commands.hybrid_command(name="rate", description="Rates something from 1 to 10.")
    async def rate(self, ctx: commands.Context, item: str):
        await ctx.send(f"{item} is rated {random.randint(1, 10)}/10.")

    @commands.hybrid_command(name="request_command", description="Ask the developers to add a new command.")
    async def request_command(self, ctx: commands.Context, description: str):
        await ctx.send("Thanks! This has been sent to the committee for review. If they like it, it will be added.")
        channel = self.bot.get_channel(committee_channel)
        await channel.send(f"New command request from {ctx.author.mention}:\n{description}")  # type: ignore

    async def wait_for_choice(self, ctx: commands.Context, choices: list[str]) -> str:
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in choices
        message = await self.bot.wait_for("message", check=check, timeout=60.0)
        return message.content.lower()


async def setup(bot: Bot):
    await bot.add_cog(GeneralCog(bot))
