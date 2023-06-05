import config
import discord

from discord import ButtonStyle
from discord.ui import View, select, Select, Button, button

class MedalsSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(MedalSelector())

class MedalSelector(Select):
    def __init__(self):
        medals = []
        for medal in config.MEDALS:
            medals.append(discord.SelectOption(label=medal["name"], emoji=medal["emoji"], value=medal["name"]))
            
        super().__init__(placeholder="Select a medal...", min_values=1, max_values=1, options=medals)

    async def callback(self, interaction: discord.Interaction):
        for medal in config.MEDALS:
            if medal["name"] == self.values[0]:
                medal_role = interaction.guild.get_role(medal["role"])
                medal_embed = discord.Embed(
                    title=medal["name"],
                    description=medal["description"],
                    color=medal["color"]
                )
                medal_embed.set_thumbnail(url=medal["icon_url"])
                # medal_embed.set_footer(text="Currently there are {} people holding this medal.".format(len(medal_role.members)))

                await interaction.response.edit_message(embed=medal_embed, view=MedalHoldersView())

class MedalHoldersView(View):
    def __init__(self):
        # self.medal_members = members
        # self.medal = medal
        super().__init__(timeout=None)

    # @button(label="Show Medal Holders", style=ButtonStyle.gray)
    # async def show_medal_holders_button(self, interaction: discord.Interaction, button: Button):
    #     members = ""
    #     for member in self.medal_members:
    #         member += "{} {}".format(config.ARROW_EMOJI, member.mention)

    #     medal_holders_embed = discord.Embed(
    #         title="{} Holders".format(self.medal["name"]),
    #         description=members,
    #         color=config.RAVEN_RED
    #     )

    #     await interaction.response.edit_message(embed=medal_holders_embed)
    
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray)
    async def medal_go_back_button(self, interaction: discord.Interaction, button: Button):
        medal_embed = discord.Embed(
            description="Please select a medal from the drop-down menu to view it's information",
            colour=config.RAVEN_RED
        )

        await interaction.response.edit_message(embed=medal_embed, view=MedalsSelectView())