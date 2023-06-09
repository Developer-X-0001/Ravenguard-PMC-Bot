import re
import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands
from Functions.SquadCodeConverter import squad_code_to_squad_name
from Functions.ColorConverter import hex_to_int

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/profiles.sqlite")

    @app_commands.command(name="profile", description="Check your\'s or someone else\'s profile.")
    async def user_profile(self, interaction: discord.Interaction, user: discord.Member=None):
        if user is None:
            user = interaction.user
        
        if user.bot:
            await interaction.response.send_message(embed=discord.Embed(description="{} You can't check on Bots!".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
            return

        data = self.database.execute("SELECT bio, color, callsign, rank, paygrade, squad, points FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()

        if data is None:
            if user.nick:
                pattern = r'\[(\w+)-(\w+)\] (\w+)'

                match = re.match(pattern, user.nick)
                if match:
                    paygrade = match.group(1)
                    squad_code = match.group(2)
                    callsign = match.group(3)
                    self.database.execute(
                        '''
                            INSERT INTO UserProfiles VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''',
                        (
                            user.id,
                            'Bio and embed color isn\'t configurable yet.',
                            hex_to_int(hex_code='FFFFFF'),
                            callsign,
                            config.RANKS[paygrade]["name"],
                            paygrade,
                            squad_code,
                            0
                        )
                    ).connection.commit()
                    data = self.database.execute("SELECT bio, color, callsign, rank, paygrade, squad, points FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()
        
        if data is not None:
            if user.nick:
                pattern = r'\[(\w+)-(\w+)\] (\w+)'

                match = re.match(pattern, user.nick)
                if match:
                    paygrade = match.group(1)
                    squad_code = match.group(2)
                    callsign = match.group(3)
                    self.database.execute(
                        '''
                            UPDATE UserProfiles SET 
                                callsign = ?,
                                rank = ?,
                                paygrade = ?,
                                squad = ?
                            WHERE user_id = ?
                        ''',
                        (
                            callsign,
                            config.RANKS[paygrade]["name"],
                            paygrade,
                            squad_code,
                            user.id,
                        )
                    ).connection.commit()
                    data = self.database.execute("SELECT bio, color, callsign, rank, paygrade, squad, points FROM UserProfiles WHERE user_id = ?", (user.id,)).fetchone()

        user_database = sqlite3.connect("./Databases/UserData/{}.sqlite".format(user.id)).execute(
            '''
                CREATE TABLE IF NOT EXISTS Medals (
                    name TEXT,
                    emoji TEXT,
                    Primary Key (name)
                )
            '''
        ).execute(
            '''
                CREATE TABLE IF NOT EXISTS Ribbons (
                    name TEXT,
                    emoji TEXT,
                    Primary Key (name)
                )
            '''
        )

        medals = ""
        for medal in config.MEDALS:
            medal_role = interaction.guild.get_role(medal["role"])
            if medal_role in user.roles:
                medals += medal["emoji"]

        ribbons = ""
        ribbons_data = user_database.execute("SELECT emoji FROM Ribbons").fetchall()
        for ribbon in ribbons_data:
            ribbons += ribbon[0]
        
        profile_embed = discord.Embed(
            title="{}'s Profile".format(user.name),
            description="Bio not set" if data[0] is None else data[0],
            color=config.RAVEN_RED if data[1] is None else data[1]
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
            value=data[3],
            inline=False
        )
        profile_embed.add_field(
            name="Callsign:",
            value=data[2],
            inline=True
        )
        profile_embed.add_field(
            name="Paygrade:",
            value=data[4],
            inline=True
        )
        profile_embed.add_field(
            name="Squad:",
            value="None" if data[5] == '00' else data[5]
        )
        profile_embed.add_field(
            name="Points",
            value=data[6],
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
            value="None" if ribbons == "" else ribbons,
            inline=False
        )
        profile_embed.set_thumbnail(url=config.RANKS[data[4]]['url'])
        profile_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        await interaction.response.send_message(embed=profile_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))