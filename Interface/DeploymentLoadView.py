import config
import sqlite3
import discord

from discord import ButtonStyle
from discord.ui import Select, select, View, Button, button

database = sqlite3.connect("./Databases/deployments.sqlite")

class DeploymentSelectView(View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.add_item(DeploymentSelector(guild=guild))

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
            value=ping.mention,
            inline=False
        )
        deployment_embed.add_field(
            name="Time:",
            value="<t:{timestamp}:F> (<t:{timestamp}:R>)".format(timestamp=time),
            inline=False
        )
        deployment_embed.add_field(
            name="Code:",
            value=code,
            inline=False
        )
        deployment_embed.add_field(
            name="Team:",
            value="None" if team is None else ":{team}_circle: {team}".format(team=team),
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

        await interaction.response.send_message(embed=deployment_embed, view=DeploymentLoadFinalView(code=self.values[0]))

class DeploymentLoadFinalView(View):
    def __init__(self, code: str):
        self.deployment_code = code
        super().__init__(timeout=None)

    @button(label="Delete", emoji=config.DELETE_EMOJI, style=ButtonStyle.gray)
    async def deployment_delete_button(self, interaction: discord.Interaction, button: Button):
        deployment_embed = discord.Embed(
            description="{} **Deployment Deleted**".format(config.DELETE_EMOJI),
            color=config.RAVEN_RED
        )
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
        self.deployment_delete_button.disabled = True
        self.deployment_send_button.disabled = True

        self.deployment_send_button.style = ButtonStyle.red
        self.deployment_send_button.label = "Sent"

        data = database.execute("SELECT ping FROM Deployments WHERE deployment_id = ?", (self.deployment_code,)).fetchone()
        ping_role = interaction.guild.get_role(data[0])
        await deployment_channel.send(embed=interaction.message.embeds[0], content=ping_role.mention)
        await interaction.response.edit_message(embed=deployment_embed, view=self)