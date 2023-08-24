#basic module to set up database and what not
import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.interactions import Interaction



from database import Database



class setupGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="setup", description="setup commands")


# modals for setup procedures
class welcomeSetupContent(ui.Modal):
    def __init__(self, message:discord.Message):
        self.message = message
        super().__init__(title="Welcome Config", timeout=180)
    content = ui.TextInput(label="Content", style=discord.TextStyle.paragraph, placeholder="The message that will be sent")
    async def on_submit(self, interaction:discord.Interaction):
        await self.message.edit(content=self.content)
        await interaction.response.send_message("Change made succesfully!", ephemeral=True)

class welcomeSetupEmbed(ui.Modal):
    def __init__(self, message:discord.Message):
        self.message = message
        super().__init__(title="Welcome Config", timeout=180)
    etitle = ui.TextInput(label="Title", style=discord.TextStyle.short, placeholder="The title of the embed")
    description = ui.TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="the embeds description")
    async def on_submit(self, interaction:discord.Interaction):
        # when creating an embed, we need to see if content was made, if not, remove the default "empty message object"
        embed = discord.Embed(title=self.etitle, description=self.description)
        await self.message.edit(embed=embed)
        await interaction.response.send_message("Change made succesfully!", ephemeral=True)



# SelectViews for setup procedures
class WelcomeSelect(ui.Select):
    def __init__(self, message):
        self.message = message

        options = [
            discord.SelectOption(label="Message Content", description="The actual message that gets sent", value="content"),
            discord.SelectOption(label="Emebed", description="Opens up the embed creators", value="embed")
        ]

        super().__init__(placeholder="edit the welcome message", min_values=0, max_values=1, options=options)
    
    async def callback(self, interaction: Interaction):
        if self.values[0] == "content":
            await interaction.response.send_modal(welcomeSetupContent(self.message))
        if self.values[0] == "embed":
            await interaction.response.send_modal(welcomeSetupEmbed(self.message))


# Views for setup procedures
class WelcomeView(ui.View):
    def __init__(self, message):
        super().__init__()
        self.add_item(WelcomeSelect(message))


# The actual Setup class that contains the setup commands
class Setup(commands.Cog):
    def __init__(self) -> None:
        super().__init__()

    
    g = setupGroup()
    # the plan for this is to have a select menu, inside are options like "content" (will open modal) and "add embed" (will open another modal) and it will live-edit the original message to show what the welcome message will become,, I need to configure the database for this lol
    @g.command()
    async def welcome(self, inte:discord.Interaction):
        #first send the default messages
        await inte.response.send_message("-----Message Starts Here-----")
        message = await inte.channel.send("[Empty Message Object]")
        await inte.channel.send("-----Message Ends Here-----\nAbove is your Welcome message! use this select menu to edit a part of the message",view=WelcomeView(message))

