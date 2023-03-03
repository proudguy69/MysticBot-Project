import discord
from discord.ext import commands
import math
import aiosqlite
import json

#import modules
from modules.community.welcome import Welcome


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='-', intents=discord.Intents.all())

    
    async def setup_hook(self):
        await self.add_cog(Welcome())
        print('bot is online!')
        return await super().setup_hook()

bot = Bot()


@bot.command()
async def ping(ctx):
    lataency = math.floor(bot.latency * 1000)
    msg = f"Pong! <:PPH1:981361257057751081>\n**Ping:** `{lataency}ms`"
    await ctx.send(msg)

@bot.command()
async def table(ctx, type):
    if type == "create":
        db = await aiosqlite.connect('../test.sqlite3')
        cussor = await db.cursor()
        await cussor.execute('CREATE TABLE IF NOT EXISTS test (msg TEXT) ')
        await cussor.close()
        await db.commit()
        await db.close()
    if type == "delete":
        db = await aiosqlite.connect('../test.sqlite3')
        cussor = await db.cursor()
        await cussor.execute('DROP TABLE test')
        await cussor.close()
        await db.commit()
        await db.close()
        
f = open('../settings.json')
data = json.load(f)

bot.run(data['TOKEN'])