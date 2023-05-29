import os
import config
import sqlite3
import discord
from discord.ext import commands

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
                    points INTEGER,
                    rank TEXT,
                    Primary Key (user_id)
                )
            '''
        ).close()
        for filename in os.listdir("./Commands"):
            if filename.endswith('.py'):
                await self.load_extension('Commands.{}'.format(filename[:-3]))
                print("Loaded {}".format(filename))

            if filename.startswith('__'):
                pass

        for filename in os.listdir("./Events"):
            if filename.endswith('.py'):
                await self.load_extension('Events.{}'.format(filename[:-3]))
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