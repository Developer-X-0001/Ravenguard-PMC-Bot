import config
import discord

from discord import ButtonStyle
from discord.ui import Button, View, button

class ApplicationButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Accept", emoji=config.DONE_EMOJI, style=ButtonStyle.gray, custom_id="accept_button")
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        application_embed = interaction.message.embeds[0]
        callsign = application_embed.fields[2].value
        user = interaction.message.mentions[0]

        verified_role = interaction.guild.get_role(config.VERIFIED_ROLE_ID)
        enlisted_role = interaction.guild.get_role(config.ENLISTED_ROLE_ID)
        pigeon_div_role = interaction.guild.get_role(config.PIGEON_DIVISION_ROLE_ID)
        cadet_role = interaction.guild.get_role(config.RANKS["T9"]["id"])

        await user.remove_roles(verified_role)
        await user.add_roles(enlisted_role)
        await user.add_roles(pigeon_div_role)
        await user.add_roles(cadet_role)
        await user.edit(nick="[T9-00] {}".format(callsign))

        self.accept_button.disabled = True
        self.reject_button.disabled = True

        self.accept_button.style = ButtonStyle.red
        self.accept_button.label = "Accepted"

        application_embed.set_footer(text="Application accepted!")
        await interaction.response.edit_message(embed=application_embed, view=self)
    
    @button(label="Reject", emoji=config.ERROR_EMOJI, style=ButtonStyle.gray, custom_id="reject_button")
    async def reject_button(self, interaction: discord.Interaction, button: Button):
        application_embed = interaction.message.embeds[0]
        self.accept_button.disabled = True
        self.reject_button.disabled = True

        self.reject_button.style = ButtonStyle.red
        self.reject_button.label = "Rejected"

        application_embed.set_footer(text="Application rejected!")
        await interaction.response.edit_message(embed=application_embed, view=self)