#Needs to be reworked

import discord
from discord.ext import commands
from discord import app_commands
import time
import random
import math
import json


class LevelFuncs():
    pass



        




class Levels(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.Cog.listener("on_message")
    async def levelslistener(self, msg:discord.Message):
        pass

    


    @app_commands.command(description="View the level of yourself or another user")
    async def level(self, interaction:discord.Interaction, user:discord.Member=None, display:bool=False):
        if not user: user=interaction.user

        data = LevelFuncs.getLevel(user.id)
        level = data["level"]
        xp = data["xp"]
        embed = discord.Embed(title=f"Level information for {user.display_name}", description=f"Level: `{level}`\nXP:`{xp}`\nXP needed: `{level*100}`\n\nGain More level by talking!", color=0xffa1dc)
        await interaction.response.send_message(embed=embed, ephemeral=display)
        
