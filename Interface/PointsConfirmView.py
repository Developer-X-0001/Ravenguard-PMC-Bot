import re
import config
import sqlite3
import discord
import asyncio

from discord import ButtonStyle
from discord.ui import Button, button, View

database = sqlite3.connect("./Databases/profiles.sqlite")

class PointsConfirmButtons(View):
    def __init__(self, message: discord.Message):
        self.original_message = message
        super().__init__(timeout=None)
    
    @button(label="Confirm", emoji=config.DONE_EMOJI, style=ButtonStyle.gray)
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        embed = interaction.message.embeds[0]
        embed.title = "Changes in Progress"
        embed.footer.text = "Please don't close this message."
        self.confirm_button.disabled = True
        self.confirm_button.label = "Updating Data..."
        self.confirm_button.emoji = config.LOAD_EMOJI
        await interaction.response.edit_message(embed=embed, view=self)

        matches = re.findall(r"\d+\+", self.original_message.content)
        users = self.original_message.mentions
        for match in matches:
            user = users[matches.index(match)]
            rank = 'T9-00'

            if user.nick:
                pattern = r'\b[A-Za-z0-9]{1,3}-[A-Za-z0-9]{1,3}\b'
                rank_match = re.findall(pattern=pattern, string=user.nick)
                rank = 'T9-00' if rank_match == [] else rank_match[0]

            database.execute("INSERT INTO UserProfiles VALUES (?, ?, ?) ON CONFLICT (user_id) DO UPDATE SET points = points + ?, rank = ? WHERE user_id = ?",
                             (user.id, int(match[:-1]), rank, int(match[:-1]), rank, user.id,)).connection.commit()
        
        await asyncio.sleep(1)
        await interaction.edit_original_response(embed=discord.Embed(description="{} Update successful!".format(config.DONE_EMOJI), color=config.RAVEN_RED), view=None)
