import re
import config
import sqlite3
import discord
import datetime

from discord.ext import commands
from discord import ButtonStyle, TextStyle
from Functions.GenerateCode import generate_unique_code
from Interface.DeploymentButtons import DeploymentButtons
from discord.ui import button, Button, View, select, Select, UserSelect, RoleSelect, TextInput, Modal, RoleSelect, ChannelSelect

database = sqlite3.connect("./Databases/deployments.sqlite")

class DeploymentStartView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Next", style=ButtonStyle.gray)
    async def deployment_next(self, interaction: discord.Interaction, button: Button):
        deployment_code = generate_unique_code()
        deployment_embed = discord.Embed(
            title="Ravenguard Deployment",
            color=config.RAVEN_RED
        )
        deployment_embed.add_field(
            name="Host: (You are the Host)",
            value=interaction.user.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Co-Host:",
            value="None",
            inline=False
        )
        deployment_embed.set_thumbnail(url=config.RAVEN_ICON)
        deployment_embed.set_footer(text="Please select the Co-Host (Optional)")

        database.execute("INSERT INTO Deployments VALUES (?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (deployment_code, interaction.user.id,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentCoHostViews(code=deployment_code))

class DeploymentCoHostViews(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @select(cls=UserSelect, placeholder="Choose a Co-Host...", row=0)
    async def co_host_select(self, interaction: discord.Interaction, select: UserSelect):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=0,
            name="Host:",
            value=interaction.user.mention,
            inline=False
        )
        deployment_embed.set_field_at(
            index=1,
            name="Co-Host:",
            value=select.values[0].mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Supervisor:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please select the Supervisor (Optional)")
        database.execute("UPDATE Deployments SET cohost_id = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=None)
        await interaction.edit_original_response(view=DeploymentSupervisorViews(code=self.deployment_code))

    @button(label="Skip", style=ButtonStyle.gray)
    async def co_host_skip(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=0,
            name="Host:",
            value=interaction.user.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Supervisor:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please select the Supervisor (Optional)")
        database.execute("UPDATE Deployments SET cohost_id = ? WHERE deployment_id = ?", ('None', self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=None)
        await interaction.edit_original_response(view=DeploymentSupervisorViews(code=self.deployment_code))

    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentSupervisorViews(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @select(cls=UserSelect, placeholder="Choose your Supervisor...", row=0)
    async def supervisor_select(self, interaction: discord.Interaction, select: UserSelect):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=2,
            name="Supervisor:",
            value=select.values[0].mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Spawn:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please select spawn location.")
        database.execute("UPDATE Deployments SET supervisor_id = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=None)
        await interaction.edit_original_response(view=DeploymentSpawnSelect(code=self.deployment_code))

    @button(label="Skip", style=ButtonStyle.gray)
    async def supervisor_skip(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=2,
            name="Supervisor:",
            value="None",
            inline=False
        )
        deployment_embed.add_field(
            name="Spawn:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please select spawn location.")
        database.execute("UPDATE Deployments SET supervisor_id = ? WHERE deployment_id = ?", ('None', self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=None)
        await interaction.edit_original_response(view=DeploymentSpawnSelect(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentSpawnSelect(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
        self.add_item(SpawnSelector(code=code))

    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray, row=1)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class SpawnSelector(Select):
    def __init__(self, code: str):
        self.deployment_code = code
        
        spawn_locations = [
            discord.SelectOption(label="FOB", description="Forward Operating Base", value="FOB"),
            discord.SelectOption(label="U.N. Checkpoint", value="U.N. Checkpoint"),
            discord.SelectOption(label="Sochraina City", value="Sochraina City")
        ]

        super().__init__(placeholder="Choose deployment spawn location...", min_values=1, max_values=1, options=spawn_locations, row=0)
    
    async def callback(self, interaction: discord.Interaction):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=3,
            name="Spawn:",
            value=self.values[0],
            inline=False
        )
        deployment_embed.add_field(
            name="Type:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please specify deployment type.")
        database.execute("UPDATE Deployments SET spawn = ? WHERE deployment_id = ?", (str(self.values[0]), self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentTypeButton(code=self.deployment_code))
    
class DeploymentTypeButton(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @button(label="Edit Deployment Type", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray)
    async def deployment_type_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentTypeModal(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentTypeModal(Modal, title="Deployment Type"):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

        self.deployment_type = TextInput(
            label="Type:",
            style=TextStyle.short,
            placeholder="Deployment type? e.g Patrol",
            required=True
        )

        self.add_item(self.deployment_type)

    async def on_submit(self, interaction: discord.Interaction):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=4,
            name="Type:",
            value=self.deployment_type.value,
            inline=False
        )
        deployment_embed.add_field(
            name="Ping:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please select a role to ping for this deployment.")
        database.execute("UPDATE Deployments SET type = ? WHERE deployment_id = ?", (self.deployment_type.value, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=None)
        await interaction.edit_original_response(view=DeploymentPingSelect(code=self.deployment_code))

class DeploymentPingSelect(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

    @select(cls=RoleSelect, placeholder="Choose a role to ping...", min_values=1, max_values=1)
    async def deployment_role_select(self, interaction: discord.Interaction, select: RoleSelect):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=5,
            name="Ping:",
            value=select.values[0].mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Time:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please set a time, timestamp required.")
        database.execute("UPDATE Deployments SET ping = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentTimeButton(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentTimeButton(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @button(label="Edit Time", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray)
    async def deployment_time_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentTimeModal(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentTimeModal(Modal, title="Deployment Time"):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

        self.deployment_time = TextInput(
            label="Timestamp:",
            style=TextStyle.short,
            placeholder="e.g {}".format(round(datetime.datetime.now().timestamp())),
            min_length=10,
            max_length=10,
            required=True
        )

        self.add_item(self.deployment_time)
    
    async def on_submit(self, interaction: discord.Interaction):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=6,
            name="Time:",
            value="<t:{timestamp}:F> (<t:{timestamp}:R>)".format(timestamp=self.deployment_time.value),
            inline=False
        )
        deployment_embed.add_field(
            name="Code:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please submit private server code.")

        database.execute("UPDATE Deployments SET time = ? WHERE deployment_id = ?", (int(self.deployment_time.value), self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentCodeButton(code=self.deployment_code))

class DeploymentCodeButton(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

    @button(label="Edit Server Code", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray)
    async def deployment_code_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentCodeModal(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentCodeModal(Modal, title="Deployment Server Code"):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
        self.deployment_server_code = TextInput(
            label="Code:",
            style=TextStyle.short,
            placeholder="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
            min_length=36,
            max_length=36,
            required=True
        )
    
        self.add_item(self.deployment_server_code)

    async def on_submit(self, interaction: discord.Interaction):
        pattern = r'^[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}$'

        match = re.match(pattern, self.deployment_server_code.value)
        if match:
            deployment_embed = interaction.message.embeds[0]
            deployment_embed.set_field_at(
                index=7,
                name="Code:",
                value=self.deployment_server_code.value,
                inline=False
            )
            deployment_embed.add_field(
                name="Team:",
                value="None",
                inline=False
            )
            deployment_embed.set_footer(text="Please choose the team for deployment.")
            database.execute("UPDATE Deployments SET code = ? WHERE deployment_id = ?", (self.deployment_server_code.value, self.deployment_code,)).connection.commit()

            await interaction.response.edit_message(embed=deployment_embed, view=None)
            await interaction.edit_original_response(view=DeploymentTeamSelect(code=self.deployment_code))
        else:
            await interaction.response.send_message(embed=discord.Embed(description="{} **Invalid Code Format!**\n```\nXXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX\n```".format(config.WARN_EMOJI), color=config.RAVEN_RED), ephemeral=True)

class DeploymentTeamSelect(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
        self.add_item(TeamSelector(code=code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray, row=1)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class TeamSelector(Select):
    def __init__(self, code: str):
        self.deployment_code = code
        
        team_colors = [
            discord.SelectOption(label="Orange", emoji="🟠", description="Orange team", value="orange"),
            discord.SelectOption(label="Green", emoji="🟢", description="Green team", value="green"),
            discord.SelectOption(label="Blue", emoji="🔵", description="Blue team", value="blue"),
            discord.SelectOption(label="Yellow", emoji="🟡", description="Yellow team", value="yellow"),
            discord.SelectOption(label="Red", emoji="🔴", description="Red team", value="red")
        ]

        super().__init__(placeholder="Choose deployment team color...", min_values=1, max_values=1, options=team_colors, row=0)
    
    async def callback(self, interaction: discord.Interaction):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=8,
            name="Team:",
            value=f":{self.values[0]}_circle: {str(self.values[0]).capitalize()}"
        )
        deployment_embed.add_field(
            name="Comms:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please select a comms channel.")
        database.execute("UPDATE Deployments SET team = ? WHERE deployment_id = ?", (self.values[0], self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=None)
        await interaction.edit_original_response(view=DeploymentCommsSelect(code=self.deployment_code))

class DeploymentCommsSelect(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.voice], placeholder="Select a comms channel...", min_values=1, max_values=1)
    async def deployment_channel_select(self, interaction: discord.Interaction, select: ChannelSelect):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=9,
            name="Comms:",
            value=select.values[0].mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Notes:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please add notes to the deployment. (Optional)")
        database.execute("UPDATE Deployments SET comms = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentNotesView(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentNotesView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @button(label="Edit Note", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray)
    async def deployment_note_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentNotesModal(code=self.deployment_code))

    @button(label="Skip", style=ButtonStyle.gray)
    async def deployment_note_skip_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=10,
            name="Notes:",
            value="None",
            inline=False
        )
        deployment_embed.add_field(
            name="Restrictions:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please add deployment restrictions.")
        database.execute("UPDATE Deployments SET notes = ? WHERE deployment_id = ?", ('None', self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentRestrictionsView(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentNotesModal(Modal, title="Deployment Notes"):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

        self.deployment_notes = TextInput(
            label="Notes:",
            style=TextStyle.long,
            placeholder="Enter deployment notes...",
            required=True
        )

        self.add_item(self.deployment_notes)

    async def on_submit(self, interaction: discord.Interaction):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=10,
            name="Notes:",
            value=self.deployment_notes.value,
            inline=False
        )
        deployment_embed.add_field(
            name="Restrictions:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please add deployment restrictions.")
        database.execute("UPDATE Deployments SET notes = ? WHERE deployment_id = ?", (self.deployment_notes.value, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentRestrictionsView(code=self.deployment_code))

class DeploymentRestrictionsView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @button(label="Edit Restrictions", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray)
    async def deployment_restrictions_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentRestrictionsModal(code=self.deployment_code))

    @button(label="Skip", style=ButtonStyle.gray)
    async def deployment_restrictions_skip_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=11,
            name="Restrictions:",
            value="None",
            inline=False
        )
        deployment_embed.add_field(
            name="Restrictions:",
            value="None",
            inline=False
        )
        deployment_embed.set_footer(text="Please add deployment restrictions.")
        database.execute("UPDATE Deployments SET notes = ? WHERE deployment_id = ?", ('None', self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentCreateFinalView(code=self.deployment_code))
    
    @button(label="Cancel", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray)
    async def deployment_cancel_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Prompt Cancelled**".format(config.ERROR_EMOJI),
            color=config.RAVEN_RED
        )
        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=None)

class DeploymentRestrictionsModal(Modal, title="Deployment Restricions"):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

        self.deployment_restrictions = TextInput(
            label="Restricions:",
            style=TextStyle.long,
            placeholder="Enter deployment restricions...",
            required=True
        )

        self.add_item(self.deployment_restrictions)

    async def on_submit(self, interaction: discord.Interaction):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=11,
            name="Restrictions:",
            value=self.deployment_restrictions.value,
            inline=False
        )
        deployment_embed.footer.text = None
        database.execute("UPDATE Deployments SET notes = ? WHERE deployment_id = ?", (self.deployment_restrictions.value, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentCreateFinalView(code=self.deployment_code))

class DeploymentCreateFinalView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @button(label="Save", emoji=config.SAVE_EMOJI, style=ButtonStyle.gray)
    async def deployment_save_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Deployment Saved**\n**Deployment ID:** `{}`".format(config.SAVE_EMOJI, self.deployment_code),
            color=config.RAVEN_RED
        )
        self.deployment_save_button.disabled = True
        self.deployment_delete_button.disabled = True
        self.deployment_send_button.disabled = True

        self.deployment_save_button.style = ButtonStyle.red
        self.deployment_save_button.label = "Saved"

        await interaction.response.edit_message(embed=deployment_embed, view=self)

    @button(label="Delete", emoji=config.DELETE_EMOJI, style=ButtonStyle.gray)
    async def deployment_delete_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Deployment Deleted**".format(config.DELETE_EMOJI),
            color=config.RAVEN_RED
        )
        self.deployment_save_button.disabled = True
        self.deployment_delete_button.disabled = True
        self.deployment_send_button.disabled = True

        self.deployment_delete_button.style = ButtonStyle.red
        self.deployment_delete_button.label = "Deleted"

        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=self)

    @button(label="Send", emoji=config.SEND_EMOJI, style=ButtonStyle.gray)
    async def deployment_send_button(self, interaction: discord.Interaction, button: Button):
        deployment_channel = interaction.guild.get_channel(config.DEPLOYMENT_CHANNEL_ID)
        deployment_embed = discord.Embed(
            description="**Deployment Sent**\n**Deployment ID:** `{}`\n**Deployment Channel:** {}".format(self.deployment_code, deployment_channel.mention),
            color=config.RAVEN_RED
        )
        self.deployment_save_button.disabled = True
        self.deployment_delete_button.disabled = True
        self.deployment_send_button.disabled = True

        self.deployment_send_button.style = ButtonStyle.red
        self.deployment_send_button.label = "Sent"

        data = database.execute("SELECT ping FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).fetchone()
        ping_role = interaction.guild.get_role(data[0])
        await deployment_channel.send(embed=interaction.message.embeds[0].set_footer(text=self.deployment_code), content=ping_role.mention, view=DeploymentButtons())
        sqlite3.connect("./Databases/Deployments/{}.sqlite".format(self.deployment_code)).execute(
            '''
                CREATE TABLE IF NOT EXISTS Joining (
                    user_id INTEGER,
                    Primary Key (user_id)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS Maybe (
                    user_id INTEGER,
                    Primary Key (user_id)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS NotJoining (
                    user_id INTEGER,
                    Primary Key (user_id)
                )
            '''
        ).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=self)