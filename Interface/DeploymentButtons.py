import config
import sqlite3
import discord

from discord import ButtonStyle
from discord.ui import Button, button, View

class DeploymentButtons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Joining (0)", emoji=config.DONE_EMOJI, style=ButtonStyle.gray, custom_id="joining_button")
    async def joining_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        deployment_code = deployment_embed.footer.text
        database = sqlite3.connect("./Databases/Deployments/{}.sqlite".format(deployment_code))
        # joining_data = database.execute("SELECT user_id FROM Joining WHERE user_id = ?", (interaction.user.id,)).fetchone()
        # maybe_data = database.execute("SELECT user_id FROM Maybe WHERE user_id = ?", (interaction.user.id,)).fetchone()
        # not_joining_data = database.execute("SELECT user_id FROM NotJoining WHERE user_id = ?", (interaction.user.id,)).fetchone()

        database.execute(
            "INSERT OR IGNORE INTO Joining VALUES (?)", (interaction.user.id,)
        ).execute(
            "DELETE FROM Maybe WHERE user_id = ?", (interaction.user.id,)
        ).execute(
            "DELETE FROM NotJoining WHERE user_id = ?", (interaction.user.id,)
        ).connection.commit()

        joining_data = database.execute("SELECT user_id FROM Joining").fetchall()
        maybe_data = database.execute("SELECT user_id FROM Maybe").fetchall()
        not_joining_data = database.execute("SELECT user_id FROM NotJoining").fetchall()

        self.joining_button.label = "Joining ({})".format(len(joining_data))
        self.maybe_button.label = "Maybe ({})".format(len(maybe_data))
        self.not_joining_button.label = "Not Joining ({})".format(len(not_joining_data))

        await interaction.response.edit_message(view=self)

    @button(label="Maybe (0)", emoji=config.MAYBE_EMOJI, style=ButtonStyle.gray, custom_id="maybe_button")
    async def maybe_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        deployment_code = deployment_embed.footer.text
        database = sqlite3.connect("./Databases/Deployments/{}.sqlite".format(deployment_code))

        database.execute(
            "INSERT OR IGNORE INTO Maybe VALUES (?)", (interaction.user.id,)
        ).execute(
            "DELETE FROM Joining WHERE user_id = ?", (interaction.user.id,)
        ).execute(
            "DELETE FROM NotJoining WHERE user_id = ?", (interaction.user.id,)
        ).connection.commit()

        joining_data = database.execute("SELECT user_id FROM Joining").fetchall()
        maybe_data = database.execute("SELECT user_id FROM Maybe").fetchall()
        not_joining_data = database.execute("SELECT user_id FROM NotJoining").fetchall()

        self.joining_button.label = "Joining ({})".format(len(joining_data))
        self.maybe_button.label = "Maybe ({})".format(len(maybe_data))
        self.not_joining_button.label = "Not Joining ({})".format(len(not_joining_data))

        await interaction.response.edit_message(view=self)

    @button(label="Not Joining (0)", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray, custom_id="not_joining_button")
    async def not_joining_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        deployment_code = deployment_embed.footer.text
        database = sqlite3.connect("./Databases/Deployments/{}.sqlite".format(deployment_code))

        database.execute(
            "INSERT OR IGNORE INTO NotJoining VALUES (?)", (interaction.user.id,)
        ).execute(
            "DELETE FROM Maybe WHERE user_id = ?", (interaction.user.id,)
        ).execute(
            "DELETE FROM Joining WHERE user_id = ?", (interaction.user.id,)
        ).connection.commit()

        joining_data = database.execute("SELECT user_id FROM Joining").fetchall()
        maybe_data = database.execute("SELECT user_id FROM Maybe").fetchall()
        not_joining_data = database.execute("SELECT user_id FROM NotJoining").fetchall()

        self.joining_button.label = "Joining ({})".format(len(joining_data))
        self.maybe_button.label = "Maybe ({})".format(len(maybe_data))
        self.not_joining_button.label = "Not Joining ({})".format(len(not_joining_data))

        await interaction.response.edit_message(view=self)
