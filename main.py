import os
import config
import sqlite3
import discord

from discord.ext import commands
from Interface.DeploymentButtons import DeploymentButtons
from Interface.ApplicationButtons import ApplicationButtons

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config.PREFIX,
            intents=intents,
            application_id=config.APPLICATION_ID
        )

    async def setup_hook(self):
        sqlite3.connect("./Databases/profiles.sqlite").execute(
            '''
                CREATE TABLE IF NOT EXISTS UserProfiles (
                    user_id INTEGER,
                    bio TEXT,
                    color INTEGER,
                    callsign TEXT,
                    rank TEXT,
                    paygrade TEXT,
                    squad TEXT,
                    points INTEGER,
                    Primary Key (user_id)
                )
            '''
        ).close()

        sqlite3.connect("./Databases/data.sqlite").execute(
            '''
                CREATE TABLE IF NOT EXISTS LogSettings (
                    guild_id INTEGER,
                    logs_channel INTEGER,
                    status TEXT,
                    Primary Key (guild_id)
                )
            '''
        )

        sqlite3.connect("./Databases/deployments.sqlite").execute(
            '''
                CREATE TABLE IF NOT EXISTS Deployments (
                    deployment_id TEXT,
                    host_id INTEGER,
                    cohost_id INTEGER,
                    supervisor_id INTEGER,
                    spawn TEXT,
                    type TEXT,
                    ping INTEGER,
                    time INTEGER,
                    code TEXT,
                    team TEXT,
                    comms INTEGER,
                    notes TEXT,
                    restrictions TEXT,
                    started_at INTEGER,
                    ended_at INTEGER,
                    Primary Key (deployment_id)
                )
            '''
        )

        sqlite3.connect("./Databases/squads.sqlite").execute(
            '''
                CREATE TABLE IF NOT EXISTS Squads (
                    code TEXT,
                    name TEXT,
                    role_id INTEGER,
                    description TEXT,
                    purpose TEXT,
                    team_lead_id INTEGER,
                    timezone TEXT,
                    color TEXT,
                    icon TEXT,
                    Primary Key (code)
                )
            '''
        )

        self.add_view(DeploymentButtons())
        self.add_view(ApplicationButtons())

        for filename in os.listdir("./Commands"):
            if filename.endswith('.py'):
                await self.load_extension('Commands.{}'.format(filename[:-3]))
                print("Loaded {}".format(filename))

            if filename.startswith('__'):
                pass

        await bot.tree.sync()

bot = Bot()

@bot.event
async def on_ready():
    print("{} is online! Latency: {}ms".format(bot.user.name, round(bot.latency * 1000)))

@bot.command(name="reload")
async def _reload(ctx: commands.Context, folder: str, cog: str):
    await ctx.message.delete()
    try:
        await bot.reload_extension(f"{folder}.{cog}")
        await ctx.send("🔁 **{}.py** successfully reloaded!".format(cog))
    except:
        await ctx.send("⚠ Unable to reload **{}**".format(cog))


bot.run(config.TOKEN)