#basic module to set up database and what not
import discord
from discord.ext import commands
from discord import app_commands, ui


from database import Database



class setupGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="setup", description="setup commands")



class welcomeModal(ui.Modal, title="Welcome Config"):

    content = ui.TextInput(label="Content", style=discord.TextStyle.paragraph, placeholder="The message that will be sent")

    async def on_submit(self, interaction:discord.Interaction):
        await interaction.response.send_message("thanks for submitting the welcome message!")
        await Database.createWelcome_Conf(interaction.guild.id, content=self.content.value)



class Setup(commands.Cog):
    def __init__(self) -> None:
        super().__init__()

    g = setupGroup()

    # the plan for this is to have a select menu, inside are options like "content" (will open modal) and "add embed" (will open another modal) and it will live-edit the original message to show what the welcome message will become,, I need to configure the database for this lol
    @g.command()
    async def welcome(self, inte:discord.Interaction):
        await inte.response.send_modal(welcomeModal())
        await Database.createServer(inte.guild.id)    