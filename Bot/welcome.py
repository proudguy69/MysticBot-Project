#welcome module for the bot\

#I want to optimize this

import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self):
        super().__init__()

    #welcome message
    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        JOINCHANNEL = member.guild.get_channel(929889618009161762)
        server = member.guild
        JOINMESSAGE = f"""
        <:PPH1:981361257057751081> <@&1180280117952528466>  Welcome {member.mention} to {server.name}! <:PPH1:981361257057751081>
        """
        JOINEMBED = discord.Embed(description="""
        Please make sure to check out these channels:\n<#929889617837182994>\n<#1013689489396334653>\n<#929889618009161762>!\n
        Also make sure to right click the server or hold tap the icon on mobile, and press "Show all channels"
        <:PPH1:981361257057751081><:PPH1:981361257057751081><:PPH1:981361257057751081><:PPH1:981361257057751081>
        """, color=0xffa1dc)

        DMMEMBERMESSAGE = None

        DMEMBEDDESCRIPTION = f"""
        Hello! I am Kai, the bots owner, I'd like to take a moment to PLEASE ask you to stay in the server,
        I understand it may not be active at this current point in time, but feel free to chat up, someone will welcome you when they notice, Thanks.
        If you have any questions or suggestions feel free to dm or ping me, Thanks, -<@729873770990534766>
        """

        DMEMBED = discord.Embed(title=f'Welcome to {server.name}', description=DMEMBEDDESCRIPTION, color=0xffa1dc)


        await JOINCHANNEL.send(content=JOINMESSAGE, embed=JOINEMBED)
        try:
            await member.send(content=DMMEMBERMESSAGE, embed=DMEMBED)
        except discord.errors.Forbidden:
            await JOINCHANNEL.send(f"{member} has dms off!")

