import discord
from discord.ext import commands
import math
import aiosqlite
import json
import time

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



tree = bot.tree

@bot.command()
async def ping(ctx:commands.Context):
    latency = math.floor(bot.latency * 1000)
    msg = f"Pong! <:PPH1:981361257057751081>\n**Ping:** `{latency}ms`"
    await ctx.send(msg)
    await ctx.send(ctx.guild.banner)
    print(ctx.guild.banner.url)
    print(ctx.guild.banner._url)

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

@bot.command()
async def sync(ctx):
    if ctx.author.id == 729873770990534766:
        msg = await ctx.send("Syncing..")
        await tree.sync(guild=discord.Object(id=929889617128349758))
        await msg.edit(content="Completed!")
#specific to only mystic Palace
@tree.command(guild=discord.Object(id=929889617128349758))
async def banish(interaction:discord.Interaction, user:discord.Member):
    await interaction.response.defer()
    #add the banished role
    banished = interaction.guild.get_role(1081105609203654686)
    await user.edit(roles=[banished])
    #send a response and log it
    channel = interaction.guild.get_channel(929889617837182988)
    await channel.send(f'{interaction.user.mention} sent {user.mention} to <#1081105498247540796>!')
    await interaction.followup.send(f"I have sent {user.mention} to <#1081105498247540796> (go to <#1079768495807529010> to see the channel)")



f = open('../settings.json')
data = json.load(f)

bot.run(data['TOKEN'])