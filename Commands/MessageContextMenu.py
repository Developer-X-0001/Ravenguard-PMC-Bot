import re
import config
import discord
import asyncio

from discord.ext import commands
from discord import app_commands
from Interface.PointsAddView import PointsAddButton

class MessageContextMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.get_info_cmd = app_commands.ContextMenu(
            name="Get Data",
            callback=self.get_info
        )
        self.bot.tree.add_command(self.get_info_cmd)
    
    async def get_info(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(embed=discord.Embed(description="{} Finding user mentions & points...".format(config.LOAD_EMOJI), color=config.RAVEN_RED), ephemeral=True)
        await asyncio.sleep(2)
        matches = re.findall(r"\d+\+", message.content)
        if matches != []:
            await interaction.edit_original_response(embed=discord.Embed(description="{} Mentions & points found!".format(config.DONE_EMOJI), color=config.RAVEN_RED))
            await asyncio.sleep(1)
            await interaction.edit_original_response(embed=discord.Embed(description="{} Collecting data...".format(config.LOAD_EMOJI), color=config.RAVEN_RED))
            users = message.mentions
            users.reverse()
            user_data = ""
            for match in matches:
                user = users[matches.index(match)]
                user_data += f"{config.ARROW_EMOJI} **Username:** {user.mention} | **Points:** {match}\n"
            await asyncio.sleep(2)
            await interaction.edit_original_response(embed=discord.Embed(description="{} Done!".format(config.DONE_EMOJI), color=config.RAVEN_RED))
            await asyncio.sleep(1)
            await interaction.edit_original_response(embed=discord.Embed(title="User mentions & Points data", description=user_data, color=config.RAVEN_RED), view=PointsAddButton(message=message))

        else:
            await interaction.edit_original_response(embed=discord.Embed(description="{} Unable to find user mentions & points!".format(config.ERROR_EMOJI), color=config.RAVEN_RED))

async def setup(bot: commands.Bot):
    await bot.add_cog(MessageContextMenu(bot))