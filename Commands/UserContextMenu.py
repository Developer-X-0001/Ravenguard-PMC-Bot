import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands

class UserContextMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/profiles.sqlite")
        self.checkstats_cmd = app_commands.ContextMenu(
            name="Checkstats",
            callback=self.check_stats
        )
        self.bot.tree.add_command(self.checkstats_cmd)
    
    async def check_stats(self, interaction: discord.Interaction, user: discord.Member):
        if user.bot:
            await interaction.response.send_message(embed=discord.Embed(description="{} You can't check on Bots!".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
            return
        
        data = self.database.execute("SELECT points, rank FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()
        if data is None or data[0] == 0:
            error_embed = discord.Embed(
                description="User must have atleast 1 point to view stats!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed)
            return
        
        result_embed = discord.Embed(
            title="{}'s Stats".format(user.name if not user.nick else user.nick),
            description="**Points** | {}\n**Rank** | {}".format(data[0], data[1]),
            color=discord.Color.dark_red()
        )
        await interaction.response.send_message(embed=result_embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(UserContextMenu(bot))