import config
import discord
import datetime

from discord import TextStyle
from discord.ui import Modal, TextInput

class ApplicationModal(Modal, title="Ravenguard PMC Application Form"):
    def __init__(self):
        super().__init__(timeout=None)
    
        self.question_one = TextInput(
            label="What server or member you joined from?",
            style=TextStyle.short,
            placeholder="e.g PlatinumFive, Developer X#0001, etc",
            required=True
        )

        self.question_two = TextInput(
            label="Desired Callsign?",
            style=TextStyle.short,
            placeholder="e.g Fox, Jay, Andy, Eclipse, etc",
            required=True
        )

        self.question_three = TextInput(
            label="Your Playstyle?",
            style=TextStyle.short,
            placeholder="e.g Marksman, Pilot, CQB, etc",
            required=True
        )

        self.question_four = TextInput(
            label="Timezone?",
            style=TextStyle.short,
            placeholder="e.g GMT, EST, PST, etc",
            required=True
        )

        self.add_item(self.question_one)
        self.add_item(self.question_two)
        self.add_item(self.question_three)
        self.add_item(self.question_four)

    async def on_submit(self, interaction: discord.Interaction):
        application_embed = discord.Embed(
            title="Ravenguard Application",
            description="Thanks for applying for Ravenguard! Please be patient, one of the HiCOM will review your application shortly.",
            color=config.RAVEN_RED,
            timestamp=datetime.datetime.now()
        )
        application_embed.add_field(
            name="What server or member you joined from?",
            value=self.question_one.value,
            inline=False
        )
        application_embed.add_field(
            name="Desired Callsign?",
            value=self.question_two.value,
            inline=False
        )
        application_embed.add_field(
            name="Your Playstyle?",
            value=self.question_three.value,
            inline=False
        )
        application_embed.add_field(
            name="Timezone?",
            value=self.question_four.value,
            inline=False
        )

        application_channel = interaction.guild.get_channel(1112039475942543431)

        msg = await application_channel.send(content=interaction.user.mention, embed=application_embed)
        await interaction.response.send_message(content="Thanks for applying!\nYou can see your submitted application here: {}".format(msg.jump_url), ephemeral=True)