import config
import sqlite3
import discord
from discord.ext import commands
from discord import app_commands

class Checkstats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/profiles.sqlite")

    @app_commands.command(name="checkstats", description="Check your\'s or someone else\'s total points.")
    async def check_stats(self, interaction: discord.Interaction, user: discord.Member=None):
        if user is None:
            user = interaction.user

        data = self.database.execute("SELECT points, rank FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()
        if data is None or data[0] == 0:
            error_embed = discord.Embed(
                description="User must have atleast 1 point to view stats!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed)
            return
        
        result_embed = discord.Embed(
            description="**Points** | {}\n**Rank** | {}".format(data[0], data[1]),
            color=discord.Color.dark_red()
        )
        await interaction.response.send_message(embed=result_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Checkstats(bot))