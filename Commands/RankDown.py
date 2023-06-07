import re
import config
import sqlite3
import discord

from Functions.ColorConverter import hex_to_int
from discord.ext import commands
from discord import app_commands

class RankDown(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/profiles.sqlite")

    @app_commands.command(name="rankdown", description="Demote a user to a lower rank.")
    @app_commands.checks.has_role(config.BOT_OPERATOR_ROLE_ID)
    async def rank_down(self, interaction: discord.Interaction, user: discord.Member):
        RANKS = config.RANKS
        RANK_LIST = config.RANK_LIST
        if user.nick:
            pattern = r'\[(\w+)-(\w+)\] (\w+)'

            match = re.match(pattern, user.nick)
            if match:
                paygrade = match.group(1)
                squad_code = match.group(2)
                callsign = match.group(3)
                current_rank_position = RANK_LIST.index(paygrade)
                next_rank_position = current_rank_position - 1
                if next_rank_position < 0:
                    await interaction.response.send_message(embed=discord.Embed(description="{} User is at the lowest rank!".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
                    return
                else:
                    current_rank_role = interaction.guild.get_role(RANKS[paygrade]['id'])
                    next_rank_role = interaction.guild.get_role(RANKS[RANK_LIST[next_rank_position]]['id'])

                    if current_rank_role in user.roles:
                        await user.remove_roles(current_rank_role)
                        await user.add_roles(next_rank_role)
                        await user.edit(nick=f"[{RANK_LIST[next_rank_position]}-{squad_code}] {callsign}")
                        self.database.execute(
                            '''
                                INSERT INTO UserProfiles VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (user_id) DO UPDATE SET rank = ?, paygrade = ? WHERE user_id = ?
                            ''',
                            (
                                user.id,
                                'None',
                                hex_to_int(hex_code='FFFFFF'),
                                callsign,
                                RANKS[RANK_LIST[next_rank_position]]['name'],
                                RANK_LIST[next_rank_position],
                                squad_code,
                                0,
                                RANKS[RANK_LIST[next_rank_position]]['name'],
                                RANK_LIST[next_rank_position],
                                user.id,
                            )
                        ).connection.commit()
                        await interaction.response.send_message(embed=discord.Embed(description="{} Successfully updated {}'s rank.".format(config.DONE_EMOJI, user.name), color=config.RAVEN_RED), ephemeral=True)
                        return
    
    @rank_down.error
    async def rank_down_error(self, interaction: discord.Interaction, error: app_commands.errors):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
        else:
            raise Exception


async def setup(bot: commands.Bot):
    await bot.add_cog(RankDown(bot))