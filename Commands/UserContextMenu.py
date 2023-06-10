import re
import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands
from Functions.ColorConverter import hex_to_int

class UserContextMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/profiles.sqlite")
        self.profile_cmd = app_commands.ContextMenu(
            name="Check Profile",
            callback=self.profile
        )
        self.rank_up_cmd = app_commands.ContextMenu(
            name="Rank Up",
            callback=self.rank_up
        )
        self.rank_down_cmd = app_commands.ContextMenu(
            name="Rank Down",
            callback=self.rank_down
        )
        self.bot.tree.add_command(self.profile_cmd)
        self.bot.tree.add_command(self.rank_up_cmd)
        self.bot.tree.add_command(self.rank_down_cmd)
    
    async def profile(self, interaction: discord.Interaction, user: discord.Member):
            
        if user.bot:
            await interaction.response.send_message(embed=discord.Embed(description="{} You can't check on Bots!".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
            return
        
        data = self.database.execute("SELECT bio, color, points FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()

        if user.nick:
            pattern = r'\[(\w+)-(\w+)\] (\w+)'
            match = re.match(pattern, user.nick)
            if match:
                paygrade = match.group(1)
                squad_code = match.group(2)
                callsign = match.group(3)

                medals = ""
                for medal in config.MEDALS:
                    medal_role = interaction.guild.get_role(medal["role"])
                    if medal_role in user.roles:
                        medals += medal["emoji"]

                profile_embed = discord.Embed(
                    title="{}'s Profile".format(user.name),
                    description="Bio not set" if data is None else data[0],
                    color=config.RAVEN_RED if data is None else data[1]
                )
                profile_embed.add_field(
                    name="Username:",
                    value=user.name,
                    inline=False
                )
                profile_embed.add_field(
                    name="Display Name:",
                    value="None" if not user.nick else user.nick,
                    inline=False
                )
                profile_embed.add_field(
                    name="Rank:",
                    value=config.RANKS[paygrade]["name"],
                    inline=False
                )
                profile_embed.add_field(
                    name="Callsign:",
                    value=callsign,
                    inline=True
                )
                profile_embed.add_field(
                    name="Paygrade:",
                    value=paygrade,
                    inline=True
                )
                profile_embed.add_field(
                    name="Squad:",
                    value="None" if squad_code == '00' else squad_code
                )
                profile_embed.add_field(
                    name="Points",
                    value=0 if data is None else data[2],
                    inline=True
                )
                profile_embed.add_field(
                    name="Joining Date:",
                    value="<t:{}:D>".format(round(user.joined_at.timestamp())),
                    inline=True
                )
                profile_embed.add_field(
                    name="Medals:",
                    value="None" if medals == "" else medals,
                    inline=False
                )
                profile_embed.add_field(
                    name="Ribbons:",
                    value="None",
                    inline=False
                )
                profile_embed.set_thumbnail(url=config.RANKS[paygrade]['url'])
                profile_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
                await interaction.response.send_message(embed=profile_embed)
        
    async def rank_up(self, interaction: discord.Interaction, user: discord.Member):
        bot_operator_role = interaction.guild.get_role(config.BOT_OPERATOR_ROLE_ID)
        if bot_operator_role not in interaction.user.roles:
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
            return
        
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
                next_rank_position = current_rank_position + 1
                if next_rank_position > 26:
                    await interaction.response.send_message(embed=discord.Embed(description="{} User is at the highest rank!".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
                    return
                else:
                    current_rank_role = interaction.guild.get_role(RANKS[paygrade]['id'])
                    next_rank_role = interaction.guild.get_role(RANKS[RANK_LIST[next_rank_position]]['id'])

                    if current_rank_role in user.roles:
                        await user.remove_roles(current_rank_role)
                        await user.add_roles(next_rank_role)
                        await user.edit(nick=f"[{RANK_LIST[next_rank_position]}-{squad_code}] {callsign}")
                        await interaction.response.send_message(embed=discord.Embed(description="{} Successfully updated {}'s rank.".format(config.DONE_EMOJI, user.name), color=config.RAVEN_RED), ephemeral=True)
                        return
    
    async def rank_down(self, interaction: discord.Interaction, user: discord.Member):
        bot_operator_role = interaction.guild.get_role(config.BOT_OPERATOR_ROLE_ID)
        if bot_operator_role not in interaction.user.roles:
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
            return
        
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
                        await interaction.response.send_message(embed=discord.Embed(description="{} Successfully updated {}'s rank.".format(config.DONE_EMOJI, user.name), color=config.RAVEN_RED), ephemeral=True)
                        return

async def setup(bot: commands.Bot):
    await bot.add_cog(UserContextMenu(bot))