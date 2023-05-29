import discord
from discord.ext import commands
from discord import app_commands

class MessageContextMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.get_info_cmd = app_commands.ContextMenu(
            name="Get Data",
            callback=self.get_info
        )
        self.bot.tree.add_command(self.get_info_cmd)
    
    async def get_info(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(content="Hello!", ephemeral=True)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(MessageContextMenu(bot))