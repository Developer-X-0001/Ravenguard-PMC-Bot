import re
import config
import sqlite3
import discord
from discord.ext import commands

class OnMessageEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        matches = re.findall(r"\d+\+", message.content)
        users = message.mentions

        user_data = ""
        for match in matches:
            user = users[matches.index(match)]
            user_data += f"User {user.name} | Points {match}\n"

        await message.channel.send(content=user_data)

async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessageEvent(bot))