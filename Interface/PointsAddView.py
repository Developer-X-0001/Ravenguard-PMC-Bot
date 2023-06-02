import re
import config
import sqlite3
import discord

from discord import ButtonStyle
from discord.ui import Button, button, View
from Interface.PointsConfirmView import PointsConfirmButtons

database = sqlite3.connect("./Databases/profiles.sqlite")

class PointsAddButton(View):
    def __init__(self, message: discord.Message):
        self.original_message = message
        super().__init__(timeout=None)
    
    @button(label="Add Points", emoji=config.ADD_EMOJI, style=ButtonStyle.gray)
    async def points_add_button(self, interaction: discord.Interaction, button: Button):
        matches = re.findall(r"\d+\+", self.original_message.content)
        users = self.original_message.mentions

        user_data_old = ""
        for match in matches:
            user = users[matches.index(match)]
            data = database.execute("SELECT points FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()

            current_points = 0 if data is None else data[0]
            user_data_old += "{} **Username:** {} | **Old Points:** {} | **Updated Points:** {}\n".format(config.ARROW_EMOJI, user.mention, current_points, (int(current_points) + int(match[:-1])))
        
        await interaction.response.edit_message(embed=discord.Embed(title="User Data Update Confirmation", description=user_data_old, color=config.RAVEN_RED).set_footer(text="Do you want to make these changes?"), view=PointsConfirmButtons(message=self.original_message))
