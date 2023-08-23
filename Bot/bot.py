import discord
from discord.ext import commands
import math
import json
import time

#import modules
from welcome import Welcome
from anonymous import Anonymous
from eco import *
from levels import Levels



class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='-', intents=discord.Intents.all())

    
    async def setup_hook(self):
        await self.add_cog(Welcome())
        await self.add_cog(Anonymous())
        await self.add_cog(Bumping())
        await self.add_cog(Eco())
        await self.add_cog(Levels())
        print('bot is online!')
        return await super().setup_hook()

bot = Bot()

@bot.command()
async def gimme(ctx:commands.Context):
    await ctx.send(ctx.guild.banner.url)

tree = bot.tree

@bot.command()
async def ping(ctx:commands.Context):
    latency = math.floor(bot.latency * 1000)
    msg = f"Pong! <:PPH1:981361257057751081>\n**Ping:** `{latency}ms`"
    await ctx.send(msg)


@bot.command()
async def sync(ctx):
    if ctx.author.id == 729873770990534766:
        msg = await ctx.send("Syncing..")
        await tree.sync()
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