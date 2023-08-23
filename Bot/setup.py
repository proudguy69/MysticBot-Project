#basic module to set up database and what not

import discord
from discord.ext import commands
from discord import app_commands

class Setup(commands.Cog):
    def __init__(self) -> None:
        super().__init__()
    @app_commands.guild_only()
    class setup(app_commands.Group):
        pass