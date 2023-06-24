import config
import sqlite3
import discord

from discord import ButtonStyle, TextStyle
from Interface.DeploymentEditView import DeploymentLoadView
from discord.ui import Select, View, button, Button, Modal, TextInput

database = sqlite3.connect("./Databases/deployments.sqlite")

class DeploymentSelectView(View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.add_item(DeploymentSelector(guild=guild))

    @button(label="Load From Message", emoji=config.LINK_EMOJI, style=ButtonStyle.gray)
    async def load_from_message_button(self, interaction: discord.Interactionn, button: Button):
        print()

class DeploymentSelector(Select):
    def __init__(self, guild: discord.Guild):
        
        data = database.execute("SELECT deployment_id, host_id FROM Deployments").fetchall()
        deployment_options = []
        for deployment in data:
            host = guild.get_member(deployment[1])
            deployment_options.append(discord.SelectOption(label="ID: {}".format(deployment[0]), description="Host: {}".format(host.name), value=deployment[0]))

        super().__init__(placeholder="Choose a deployment...", min_values=1, max_values=1, options=deployment_options, row=0)
    
    async def callback(self, interaction: discord.Interaction):
        data = database.execute("SELECT host_id, cohost_id, supervisor_id, spawn, type, ping, time, code, team, comms, notes, restrictions FROM Deployments WHERE deployment_id = ?", (self.values[0],)).fetchone()

        host = interaction.guild.get_member(data[0])
        co_host = interaction.guild.get_member(data[1])
        supervisor = interaction.guild.get_member(data[2])
        spawn = data[3]
        type = data[4]
        ping = interaction.guild.get_role(data[5])
        time = data[6]
        code = data[7]
        team = data[8]
        comms = interaction.guild.get_channel(data[9])
        notes = data[10]
        restrictions = data[11]

        deployment_embed = discord.Embed(
            title="Ravenguard Deployment",
            color=config.RAVEN_RED
        )
        deployment_embed.add_field(
            name="Host:",
            value="None" if host is None else host.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Co-Host:",
            value="None" if co_host is None else co_host.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Supervisor:",
            value="None" if supervisor is None else supervisor.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Spawn:",
            value=spawn,
            inline=False
        )
        deployment_embed.add_field(
            name="Type:",
            value=type,
            inline=False
        )
        deployment_embed.add_field(
            name="Ping:",
            value="None" if ping is None else ping.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Time:",
            value="None" if time is None else "<t:{timestamp}:F> (<t:{timestamp}:R>)".format(timestamp=time),
            inline=False
        )
        deployment_embed.add_field(
            name="Code:",
            value=code,
            inline=False
        )
        deployment_embed.add_field(
            name="Team:",
            value="None" if team is None else f":{team}_circle: {str(team).capitalize()}",
            inline=False
        )
        deployment_embed.add_field(
            name="Comms",
            value="None" if comms is None else comms.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Notes:",
            value=notes,
            inline=False
        )
        deployment_embed.add_field(
            name="Restrictions",
            value=restrictions,
            inline=False
        )
        deployment_embed.set_thumbnail(url=config.RAVEN_ICON)
        await interaction.response.edit_message(embed=deployment_embed, view=DeploymentLoadView(code=self.values[0]))

class DeploymentLoadModal(Modal, title="Deployment Load from Message"):
    def __init__(self):
        super().__init__(timeout=None)
    
        self.message_id = TextInput(
            label="Message ID",
            style=TextStyle.short,
            placeholder="Type the id of older deployment message",
            required=True
        )

        self.add_item(self.message_id)

    async def on_submit(self, interaction: discord.Interaction):
        if self.message_id.value.isdigit():
            deployments_channel = interaction.guild.get_channel(config.DEPLOYMENT_CHANNEL_ID)
            deployment_message = await deployments_channel.fetch_message(self.message_id.value)

            if deployment_message:
                deployment_id = deployment_message.embeds[0].footer.text
                data = database.execute("SELECT deployment_id FROM Deployments WHERE deployment_id = ?", (deployment_id,)).fetchone()
                if data:
                    deployment_embed = deployment_message.embeds[0]
        
        else:
            await interaction.response.send_message(embed=discord.Embed())