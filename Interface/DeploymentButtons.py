import config
import sqlite3
import discord

from discord import ButtonStyle
from discord.ui import Button, button, View

class DeploymentButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Joining", emoji=config.DONE_EMOJI, style=ButtonStyle.gray, custom_id="joining_button")
    async def joining_button(self, interaction: discord.Interaction, button: Button):
        print()
    
    @button(label="Maybe", emoji=config.WARN_EMOJI, style=ButtonStyle.gray, custom_id="maybe_button")
    async def maybe_button(self, interaction: discord.Interaction, button: Button):
        print()
    
    @button(label="Not Joining", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray, custom_id="not_joining_button")
    async def not_joining_button(self, interaction: discord.Interaction, button: Button):
        print()