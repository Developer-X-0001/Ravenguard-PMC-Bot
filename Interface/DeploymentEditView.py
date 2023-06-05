import config
import sqlite3
import discord
import datetime

from discord import ButtonStyle, TextStyle
from discord.ui import View, Modal, TextInput, Button, Select, ChannelSelect, UserSelect, RoleSelect, button, select

database = sqlite3.connect("./Databases/deployments.sqlite")

class DeploymentEditView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

    @button(label="Edit Co-Host", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=0)
    async def deployment_edit_cohost_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditCoHostView(code=self.deployment_code))
    
    @button(label="Edit Supervisor", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=0)
    async def deployment_edit_supervisor_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditSupervisorView(code=self.deployment_code))

    @button(label="Edit Spawn", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=0)
    async def deployment_edit_spawn_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditSpawnView(code=self.deployment_code))

    @button(label="Edit Deployment Type", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=1)
    async def deployment_type_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentTypeModal(code=self.deployment_code))
    
    @button(label="Edit Ping Role", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=1)
    async def deployment_edit_ping_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditPingView(code=self.deployment_code))
    
    @button(label="Edit Time", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=1)
    async def deployment_time_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentTimeModal(code=self.deployment_code))

    @button(label="Edit Server Code", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=2)
    async def deployment_code_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentCodeModal(code=self.deployment_code))

    @button(label="Edit Team", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=2)
    async def deployment_edit_team_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditTeamView(code=self.deployment_code))

    @button(label="Edit Comms", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=2)
    async def deployment_code_comms_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditCommsView(code=self.deployment_code))

    @button(label="Edit Note", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=3)
    async def deployment_note_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentNotesModal(code=self.deployment_code))

    @button(label="Edit Restrictions", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray, row=3)
    async def deployment_restrictions_edit_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DeploymentRestrictionsModal(code=self.deployment_code))
    
    @button(label="Save", emoji=config.SAVE_EMOJI, style=ButtonStyle.gray, row=4)
    async def deployment_save_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentLoadView(code=self.deployment_code))

class DeploymentEditCoHostView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

    @select(cls=UserSelect, placeholder="Choose a Co-Host...", row=0)
    async def co_host_select(self, interaction: discord.Interaction, select: UserSelect):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=1,
            name="Co-Host:",
            value=select.values[0].mention,
            inline=False
        )
        database.execute("UPDATE Deployments SET cohost_id = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)
    
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray)
    async def deployment_edit_go_back_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditView(code=self.deployment_code))

class DeploymentEditSupervisorView(View):
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
        database.execute("UPDATE Deployments SET supervisor_id = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)
    
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray)
    async def deployment_edit_go_back_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditView(code=self.deployment_code))

class DeploymentEditPingView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

    @select(cls=RoleSelect, placeholder="Choose a role to ping...", min_values=1, max_values=1, row=0)
    async def deployment_role_select(self, interaction: discord.Interaction, select: RoleSelect):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=5,
            name="Ping:",
            value=select.values[0].mention,
            inline=False
        )
        database.execute("UPDATE Deployments SET ping = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)
    
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray)
    async def deployment_edit_go_back_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditView(code=self.deployment_code))

class DeploymentEditCommsView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
    
    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.voice], placeholder="Select a comms channel...", min_values=1, max_values=1, row=0)
    async def deployment_channel_select(self, interaction: discord.Interaction, select: ChannelSelect):
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=9,
            name="Comms:",
            value=select.values[0].mention,
            inline=False
        )
        database.execute("UPDATE Deployments SET comms = ? WHERE deployment_id = ?", (select.values[0].id, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)
    
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray)
    async def deployment_edit_go_back_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditView(code=self.deployment_code))

class DeploymentEditSpawnView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
        self.add_item(SpawnSelector(code=code))
    
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray, row=1)
    async def deployment_edit_go_back_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditView(code=self.deployment_code))

class DeploymentEditTeamView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)
        self.add_item(TeamSelector(code=code))
    
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray, row=1)
    async def deployment_edit_go_back_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=DeploymentEditView(code=self.deployment_code))

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
        database.execute("UPDATE Deployments SET spawn = ? WHERE deployment_id = ?", (str(self.values[0]), self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)

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
        database.execute("UPDATE Deployments SET team = ? WHERE deployment_id = ?", (self.values[0], self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)

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
        database.execute("UPDATE Deployments SET type = ? WHERE deployment_id = ?", (self.deployment_type.value, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)

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

        database.execute("UPDATE Deployments SET time = ? WHERE deployment_id = ?", (int(self.deployment_time.value), self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)

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
        deployment_embed = interaction.message.embeds[0]
        deployment_embed.set_field_at(
            index=7,
            name="Code:",
            value=self.deployment_server_code.value,
            inline=False
        )
        database.execute("UPDATE Deployments SET code = ? WHERE deployment_id = ?", (self.deployment_server_code.value, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)

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
        database.execute("UPDATE Deployments SET notes = ? WHERE deployment_id = ?", (self.deployment_notes.value, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)

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
        database.execute("UPDATE Deployments SET notes = ? WHERE deployment_id = ?", (self.deployment_restrictions.value, self.deployment_code,)).connection.commit()

        await interaction.response.edit_message(embed=deployment_embed)

class DeploymentLoadView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

    @button(label="Send", emoji=config.SEND_EMOJI, style=ButtonStyle.gray)
    async def deployment_send_button(self, interaction: discord.Interaction, button: Button):
        deployment_channel = interaction.guild.get_channel(config.DEPLOYMENT_CHANNEL_ID)
        deployment_embed = discord.Embed(
            description="**Deployment Sent**\n**Deployment ID:** `{}`\n**Deployment Channel:** {}".format(self.deployment_code, deployment_channel.mention),
            color=config.RAVEN_RED
        )
        self.deployment_delete_button.disabled = True
        self.deployment_send_button.disabled = True
        self.deployment_edit_button.disabled = True

        self.deployment_send_button.style = ButtonStyle.red
        self.deployment_send_button.label = "Sent"

        data = database.execute("SELECT ping FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).fetchone()
        ping_role = interaction.guild.get_role(data[0])
        await deployment_channel.send(embed=interaction.message.embeds[0], content=ping_role.mention)
        await interaction.response.edit_message(embed=deployment_embed, view=self)

    @button(label="Edit", emoji=config.EDIT_EMOJI, style=ButtonStyle.gray)
    async def deployment_edit_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = interaction.message.embeds[0]
        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentEditView(code=self.deployment_code))

    @button(label="Delete", emoji=config.DELETE_EMOJI, style=ButtonStyle.gray)
    async def deployment_delete_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Deployment Deleted**".format(config.DELETE_EMOJI),
            color=config.RAVEN_RED
        )
        self.deployment_delete_button.disabled = True
        self.deployment_send_button.disabled = True
        self.deployment_edit_button.disabled = True

        self.deployment_delete_button.style = ButtonStyle.red
        self.deployment_delete_button.label = "Deleted"

        database.execute("DELETE FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).connection.commit()
        await interaction.response.edit_message(embed=deployment_embed, view=self)