#basic module to set up database and what not
import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.interactions import Interaction



from database import Database



class setupGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="setup", description="setup commands")

# gonna move all of this to its own "Embed Creator"
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
        embed = discord.Embed(title=self.etitle, description=self.description)
        sm = WelcomeEmbedSelect(message=self.message)
        sm.add_option(label="Edit Embed 1", value="E1", description="Edit the embed")
        self.add_item(sm)
        await self.message.edit(embed=embed, view=self) # Error Here
        await interaction.response.send_message("Change made succesfully!", ephemeral=True)



# SelectViews for setup procedures

# this will be to select each message that the bot sends
class WelcomeContentSelect(ui.Select):
    def __init__(self, message):
        self.message = message

        options = [
        ]

        super().__init__(placeholder="edit the welcome message", min_values=0, max_values=1, options=options)
    
    async def callback(self, interaction: Interaction):
        pass


# this will be to select each embed
class WelcomeEmbedSelect(ui.Select):
    def __init__(self, message):
        self.message = message

        options = [
        ]

        super().__init__(placeholder="edit the welcome message", min_values=0, max_values=1, options=options)
    
    async def callback(self, interaction: Interaction):
        pass


# Views for setup procedures
class WelcomeView(ui.View):
    def __init__(self, message):
        super().__init__()
        self.message = message
    
    @ui.button(label="Edit Message", style=discord.ButtonStyle.green)
    async def content(self, inte:discord.Interaction, button:ui.Button):
        await inte.response.send_modal(welcomeSetupContent(self.message))

    
    
    @ui.button(label="Add Embed", style=discord.ButtonStyle.green)
    async def embed(self, inte:discord.Interaction, button:ui.Button):
        await inte.response.send_modal(welcomeSetupEmbed(self.message))


# The actual Setup class that contains the setup commands
class Setup(commands.Cog):
    def __init__(self) -> None:
        super().__init__()
    g = setupGroup()
    

    #initialize the server on join
    @g.command()
    async def config(self, inte:discord.Interaction):
        await inte.response.send_message("Setting up server")
        await Database.createServer()



    

    # the plan for this is to have a select menu, inside are options like "content" (will open modal) and "add embed" (will open another modal) and it will live-edit the original message to show what the welcome message will become,, I need to configure the database for this lol
    @g.command()
    async def welcome(self, inte:discord.Interaction):
        #first send the default messages
        await inte.response.send_message("-----Message Starts Here-----")
        message = await inte.channel.send("[Empty Message Object]")
        await inte.channel.send("-----Message Ends Here-----\nAbove is your Welcome message! use this select menu to edit a part of the message",view=WelcomeView(message))



