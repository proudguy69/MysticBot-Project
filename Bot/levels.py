#Needs to be reworked

import discord
from discord.ext import commands
from discord import app_commands
import time
import random
import math
import json


class LevelFuncs():


    def getLevel(uid):
        file = open("levels.json", "r")
        pdata = json.load(file); file.close()
        try: udata = pdata[f"{uid}"]
        except KeyError: udata = None
        return udata
        

    def editxp(uid, xp):
        # open files
        file = open("levels.json", "r")
        pdata = json.load(fp=file)
        file.close()

        # get the data
        try: udata = pdata[f"{uid}"]
        except KeyError: udata = {"level":1,"xp":0,"time":0}

        # set the xp
        udata["xp"] = xp

        # compress the data
        pdata[f"{uid}"] = udata
        
        # save the data
        file = open("levels.json", "w")
        json.dump(pdata, file); file.close()



    def increaseLevel(uid):
        # set vars
        state = False
        
        # load the data
        file = open("levels.json", "r")
        pdata = json.load(fp=file)
        file.close()
        
        # check the data
        try: udata = pdata[f"{uid}"]
        except KeyError: udata = {"level":1,"xp":0,"time":0}
        ctime = math.floor(time.time())

        # check if its been 60 seconds
        if ctime - udata["time"] >= 60:
            # increase xp
            cxp = udata["xp"]
            clevel = udata['level']
            xpinc = random.randint(1,(clevel*100)/4)

            if xpinc + cxp >= clevel*100:
                # increase level
                cxp = clevel%(xpinc+cxp)
                clevel +=1
                state = True
            else:
                cxp += xpinc
                state = False
            # set the values
            udata["level"] = clevel
            udata["xp"] = cxp
            udata["time"] = math.floor(time.time())
            # compress the data
            pdata[f"{uid}"] = udata
            
            # save the data
            file = open("levels.json", "w")
            json.dump(pdata, file); file.close()
            return state



        




class Levels(commands.Cog):
    def __init__(self):
        super().__init__()

    @commands.Cog.listener("on_message")
    async def levelslistener(self, msg:discord.Message):
        if msg.channel.type == discord.ChannelType.private: return
        if msg.author.bot == True: return
        if LevelFuncs.increaseLevel(msg.author.id):
            data = LevelFuncs.getLevel(msg.author.id)
            level = data["level"]
            if level == 5:
                role = msg.guild.get_role(1080550825279099011)
                msg.author.add_roles([role])

            await msg.channel.send(f"Congrats {msg.author.mention}! you are now! Level `{level}`!")

    


    @app_commands.command(description="View the level of yourself or another user")
    async def level(self, interaction:discord.Interaction, user:discord.Member=None, display:bool=False):
        if not user: user=interaction.user

        data = LevelFuncs.getLevel(user.id)
        level = data["level"]
        xp = data["xp"]
        embed = discord.Embed(title=f"Level information for {user.display_name}", description=f"Level: `{level}`\nXP:`{xp}`\nXP needed: `{level*100}`\n\nGain More level by talking!", color=0xffa1dc)
        await interaction.response.send_message(embed=embed, ephemeral=display)
        
