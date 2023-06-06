import re
import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands
from Functions.ColorConverter import hex_to_int
from Interface.PointsConfirmView import PointsConfirmButtons

database = sqlite3.connect("./Databases/profiles.sqlite")

class Points(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="addpoints", description="Add points to a user.")
    async def add_points(self, interaction: discord.Interaction, amount: int, users: str):
        pattern = r'<@(\d+)>'

        matches = re.findall(pattern, users)

        data = ""

        for match in matches:
            user = interaction.guild.get_member(int(match))
            data += "{} **Username:** {} | **Points:** {}+".format(config.ARROW_EMOJI, user.mention, amount)
            if user.nick:
                pattern = r'\[(\w+)-(\w+)\] (\w+)'

                match = re.match(pattern, user.nick)
                if match:
                    paygrade = match.group(1)
                    squad_code = match.group(2)
                    callsign = match.group(3)
                    database.execute(
                        '''
                            INSERT INTO UserProfiles VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (user_id) DO UPDATE SET points = points + ? WHERE user_id = ?
                        ''',
                        (
                            user.id,
                            'None',
                            hex_to_int(hex_code='FFFFFF'),
                            callsign,
                            config.RANKS[paygrade]["name"],
                            paygrade,
                            squad_code,
                            amount,
                            amount,
                            user.id,
                        )
                    ).connection.commit()

        points_embed = discord.Embed(
            title="Successfully Updated Points",
            description=data,
            color=config.RAVEN_RED
        )
        await interaction.response.send_message(embed=points_embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Points(bot))