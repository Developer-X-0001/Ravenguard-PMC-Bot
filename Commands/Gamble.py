import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands

class Gamble(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/profiles.sqlite")

    @app_commands.command(name="gamble", description="Play gambling with other users to get or lose points.")
    @app_commands.describe(user="The person you wanna gamble with.", amount="The amount you wanna gamble.", type="Type of gambling.")
    @app_commands.choices(type=[
        app_commands.Choice(name="Dice Roll", value="dice"),
        app_commands.Choice(name="Coin Flip", value="coin")
    ])
    async def _gamble(self, interaction: discord.Interaction, user: discord.Member, amount: int, type: app_commands.Choice[str]):
        user1_data = self.database.execute("SELECT points FROM UserProfiles WHERE user_id = ?", (interaction.user.id,)).fetchone()
        user1_points = user1_data[0] if user1_data is not None else 0

        if user1_points < amount:
            await interaction.response.send_message(embed=discord.Embed(description="{} You can't bet more than your current points!".format(config.ERROR_EMOJI), color=config.RAVEN_RED))
            return

        user2_data = self.database.execute("SELECT points FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()
        user2_points = user2_data[0] if user2_data is not None else 0

        if user2_points < amount:
            await interaction.response.send_message(embed=discord.Embed(description="{} Your opponent must have atleast {} points to gamble!".format(config.ERROR_EMOJI, amount), color=config.RAVEN_RED))
            return
    
        gamble_embed = discord.Embed(
            title="Ravenguard's Gambling",
            description="{} has challenged {} for gambling!",
            color=config.RAVEN_RED
        )
        gamble_embed.add_field(
            name="1st Candidate",
            value=interaction.user.mention,
            inline=True
        )
        gamble_embed.add_field(
            name="2nd Candidate",
            value=user.mention,
            inline=True
        )
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Gamble(bot))