import discord
from discord.ext import commands
import math
import json
import time
from discord.ext import tasks

#import modules
from welcome import Welcome
from anonymous import Anonymous
from eco import *
from levels import Levels
from setup import Setup
from message import Message



original_roles = {}
permabanned = [943609267359977552, 1118393944955420775]
banishedl = [] # use a goddamn db for persistant storage retard
# and store set variables as high as you can for readability

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='-', intents=discord.Intents.all())
    async def setup_hook(self):
        #add cogs
        await self.add_cog(Message())
        await self.add_cog(Setup())
        # await self.add_cog(Anonymous())
        # await self.add_cog(Bumping())
        # await self.add_cog(Eco()) # needs to be reworked
        # await self.add_cog(Levels()) # needs to be reworked
        print(f'{self.user} is online!')
        return await super().setup_hook()

bot = Bot()
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
        await tree.sync(guild=discord.Object(id=929889617128349758))
        await msg.edit(content="Completed!")



#specific to only mystic Palace
@tree.command(guild=discord.Object(id=929889617128349758))
async def banish(interaction:discord.Interaction, user:discord.Member):
    global original_roles

    if user.id not in original_roles: # check for if not saved already
        original_roles[user.id] = user.roles # store the persons old roles bcus fuck you

    await interaction.response.defer() # whatever this is, looks important

    if user.id not in banishedl: # add user to the banished list only if they are not in it already
        banishedl.append(user.id)
    
    # add banished role and remove others
    banished = interaction.guild.get_role(1081105609203654686)
    await user.edit(roles=[banished])
    # log to admin channel
    channel = interaction.guild.get_channel(929889617837182988)
    await channel.send(f'{interaction.user.mention} sent {user.mention} to <#1081105498247540796>!')
    await interaction.followup.send(f"I have sent {user.mention} to <#1081105498247540796> (go to <#1079768495807529010> to see the channel)")




@tree.command(guild=discord.Object(id=929889617128349758), name="unbanish")
async def unbanish(interaction:discord.Interaction, user:discord.Member):
    if user.id not in permabanned:
        global original_roles
        await interaction.response.defer()

        banished = interaction.guild.get_role(1081105609203654686)
        await user.remove_roles(banished)

        if user.id in banishedl or original_roles: # check if user is even banished and if so, restore his original roles
            await user.edit(roles=original_roles[user.id])
            del original_roles[user.id]

            while user.id in banishedl:
                banishedl.remove(user.id)
                # while loop in case the user was banished multiple times like me who is probably like 17 times in the list already 
                # which should not even happen in the first place if your code was even slightly good (i fixed it tho, you lazy ass)

            # send info to chat
            await interaction.followup.send(f"{user.display_name} has been unbanished and their roles have been restored!")

            # log to admin channel
            channel = interaction.guild.get_channel(929889617837182988)
            await channel.send(f'{interaction.user.mention} has unbanished {user.mention}!')
            await interaction.followup.send(f"I have freed {user.mention} from <#1081105498247540796>")

        else: 
            await interaction.followup.send("This user wasn't banished tho you dumbass")
            channel = interaction.guild.get_channel(929889617837182988)
            await channel.send(f'{interaction.user.mention} is a failure and didn\'t realize that {user.mention} wasn\'t banished in the first place!')
    else:
        await interaction.followup.send(f"{user.display_name} is on the permabanned list, i cannot unbanish this person.")




#reban the user when joining
@bot.listen("on_join")
async def banishjoin(member:discord.Member):
    if member.id in banishedl:
        banished = member.guild.get_role(1081105609203654686)
        await member.edit(roles=[banished])







f = open('../settings.json')
data = json.load(f)

bot.run(data['TOKEN'])
