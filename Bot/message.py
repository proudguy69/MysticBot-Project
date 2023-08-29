# this is gonna be the module for our "Message Creator", where you can create, edit, and delete custom messages w/ embeds
import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.interactions import Interaction



from database import Database




class MessageGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="message", description="Commands to create, edit, and delete custom messages")




class Message(commands.Cog):
    def __init__(self) -> None:
        super().__init__()
    # Variables
    g = MessageGroup()





    # the view class for the creation tool
    class CreateView(ui.View):
        def __init__(self):
            super().__init__(timeout=300)
        embeds = []
        content = ""




        # the modal for editing the messages content
        class CreateViewContentModal(ui.Modal):
            def __init__(self):
                super().__init__(title="Content Editor", timeout=300)
            contentMessage = ui.TextInput(label="Content", style=discord.TextStyle.paragraph, placeholder="The actual content to the message")

            async def on_submit(self, interaction:discord.Interaction):
                self.children[0].label = "Edit Content"
                await interaction.edit_original_response(view=self)
        


        # the embed editor
        class CreateViewEmbedModal(ui.Modal):
            def __init__(self):
                super().__init__(title="Embed Editor", timeout=300)
            title = ui.TextInput(label="title", style=discord.TextStyle.short, placeholder="The title of the embed")
            description = ui.TextInput(label="Description", style=discord.TextStyle.paragraph, placeholder="The desciption of the embed")




        # the button to add content
        @ui.button(label="Add Content", style=discord.ButtonStyle.green)
        async def CreateViewAddContent(self, interaction:discord.Interaction, button:discord.Button):
            modal = self.CreateViewContentModal()
            await interaction.response.send_modal(modal)
            
            


        # the button to add embeds
        @ui.button(label="Add Embed", style=discord.ButtonStyle.green)
        async def CreateViewAddEmbed(self, interaction:discord.Interaction, button:discord.Button):
            await interaction.response.send_modal(self.CreateViewEmbedModal())


        # the button to edit embeds
        @ui.button(label="Edit Embeds", style=discord.ButtonStyle.green)
        async def CreateViewEditEmbeds(self, interaction:discord.Interaction, button:discord.Button):
            await interaction.response.send_message("test", ephemeral=True)


        

    # The create command
    @g.command(name="create", description="Create a custom message")
    @app_commands.describe(name="The saved name of the message, you will use this to locate and use the message you create")
    async def create(self, interaction:discord.Interaction, name:str):
        embed = discord.Embed(title="Message Creator", description="Welcome to the message creator! Use the Buttons below to interact with the message!")
        await interaction.response.send_message(embed=embed,view=self.CreateView())
