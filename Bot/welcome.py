#welcome module for the bot
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
        <:PPH1:981361257057751081> Welcome {member.mention} to {server.name}! <:PPH1:981361257057751081>
        """
        JOINEMBED = discord.Embed(description="""
        Please make sure to check out our <#929889617837182994> and <#1079768495807529010>!Then please <#1013689489396334653> and get to chatting in <#929889618009161762>!
        <:PPH1:981361257057751081><:PPH1:981361257057751081><:PPH1:981361257057751081><:PPH1:981361257057751081>
        """, color=0xffa1dc)

        DMMEMBERMESSAGE = None

        DMEMBEDDESCRIPTION = f" Hello! I am Mystic Bot! The personal bot for {server.name}! <:PPH1:981361257057751081>\n\nPlease be paitent with our server, it's fairly small so don't expect people to me chatting all the time, If you'd like to get things going, feel free to mention @dead chat ping\nPlease note attemtping to abuse that will result in punishments. <:PPH1:981361257057751081>\n\nI, the server owner greatly appreciate you being here. If their is anything you want, or need, Please let me know. you can find and dm me here <@729873770990534766> (Napalie#0002)\nPlease do not randomly dm me, Thanks <:PPH1:981361257057751081>"
        DMEMBED = discord.Embed(title=f'Welcome to {server.name}', description=DMEMBEDDESCRIPTION, color=0xffa1dc)


        await JOINCHANNEL.send(content=JOINMESSAGE, embed=JOINEMBED)
        try:
            await member.send(content=DMMEMBERMESSAGE, embed=DMEMBED)
        except discord.errors.Forbidden:
            await JOINCHANNEL.send(f"{member} has dms off!")

