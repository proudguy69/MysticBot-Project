#basic module to set up database and what not

import discord
from discord.ext import commands
from discord import app_commands

from database import Database



class setupGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="setup", description="setup commands")



class Setup(commands.Cog):
    def __init__(self) -> None:
        super().__init__()
    g = setupGroup()

    @g.command()
    async def welcome(self, inte:discord.Interaction):
        await inte.response.send_message("This is a test with example data!")
        await Database.createServer(inte.guild.id)


    
    